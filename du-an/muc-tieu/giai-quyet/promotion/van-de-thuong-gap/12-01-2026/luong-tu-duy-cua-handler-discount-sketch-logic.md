# timeline
- sketch viết tay
- sketch logic
- code mẫu
# sketch logic

## sketch viết tay
- phase 1: kiểm tra đầu vào và kiểm duyệt thông tin hợp lệ (entry và guard)
	-> kiểm tra payload và request (đưa cái gì cho ai ở đâu)
- phase 2: lấy danh sách yêu cầu, sắp xếp theo thứ tự và ghi nhận kết quả mong đợi (aggregate root - discounttype)
	-> kiểm tra trong payload có refname = discounts
	-> lấy danh sách request của discounts sắp xếp theo (create, update, soft_delete, hard_delete)
- phase 3: tương tự phase 2 xử lý cá phần phụ thuộc dependent refs (discount, ...)

## tổng thể handler (bức tranh lớn)

- loại handler: command-driven batch handler
- phạm vi: sync discount + các ref liên quan
- chiến lược:

  * aggregate root chạy trước
  * ref phụ chạy sau
  * mọi thứ có thứ tự, không đoán mò
  * success/fail quyết ở mức job

---

## sketch xử lý (phiên bản đã sửa đúng domain)

### phase 0: entry & guard

- handler nhận:

  * request
  * payload
- nếu payload rỗng hoặc không có ref nào:

  * return sớm
- mục tiêu:

  * không chạy job vô nghĩa
  * fail sớm, fail rõ

---

### phase 1: aggregate root – discounttype

- kiểm tra payload có refname = discounttype
- nếu có:

  * lấy danh sách request
  * sắp xếp theo action:

    * create
    * update
    * soft_delete
    * hard_delete
  * execute tuần tự
  * add result vào response

**tư duy cốt lõi:**

- discounttype sinh ra ident gốc
- ident này là "cha"
- chưa có cha → con không được sinh
- chạy sai thứ tự là dữ liệu mồ côi ngay

---

### phase 2: dependent refs – discount + các ref khác

- duyệt toàn bộ payload
- bỏ qua discounttype
- với mỗi ref còn lại:

  * nếu có request:

    * sắp xếp theo action
    * execute tuần tự
    * add result theo refname

**lưu ý đặc biệt với discount:**

- discount **bắt buộc** tham chiếu discounttype.ident
- phase này giả định:

  * discounttype đã tồn tại
  * ident đã ổn định
- không validate lại quan hệ ở đây
- tin vào phase 1

---

### phase 3: execute một batch (executeRefRequestAsync)

- nếu data rỗng:

  * return result trống
- send setrefdata xuống rk7
- nếu fail:

  * fail toàn batch
- nếu success:

  * create:

    * query lại guid → ident
  * update/delete:

    * dùng ident sẵn có

**triết lý:**

- batch là đơn vị nguyên tử
- hoặc sống hết
- hoặc chết hết
- không zombie data

---

### phase 4: tổng hợp kết quả job

- flatten toàn bộ item result
- chỉ cần 1 item có errormessage:

  * successdiscount = false
- không có khái niệm "tạm ổn"

---

## bản chất kiến trúc (chốt hạ)

- đây không phải saga
- không phải event sourcing
- đây là:

  * command-driven
  * batch-oriented
  * ordered execution
  * rk7 là source of truth

nói ngắn gọn kiểu tech lead:

- **phase 1 sinh root**
- **phase 2 gắn phụ**
- **phase 3 xử lý batch**
- **phase 4 quyết định sống chết của job**

# code mẫu (ví dụ handler SaveDiscountHandler)

```c#
using RefAgent.Configuration;
using RefAgent.Helpers;
using RefAgent.Models;
using RefAgent.Models.Request;
using RefAgent.Models.Request.Discount;
using RefAgent.Models.Response.Discount;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace RefAgent.Services.Handlers.Discount
{
    public class SaveDiscountHandler : BaseActNameHandler<DiscountRequestModel>
    {
        public SaveDiscountHandler(IRk7Services rk7Services, AppSettings appSettings)
            : base(rk7Services, appSettings)
        {
        }

        public override string ActName => Constants.ActNames.SaveDiscount;

        protected override async Task<IHandlerResult> ExecuteCoreAsync(
            SetRefDataRequest request,
            DiscountRequestModel payload,
            CancellationToken cancellationToken = default)
        {
            try
            {
                var response = new DiscountResponseModel
                {
                    SyncTaskId = payload?.SyncTaskId ?? 0
                };

                if (payload?.Discounts == null || payload.Discounts.Count == 0)
                {
                    response.SuccessDiscount = false;
                    return HandlerResult<DiscountResponseModel>.CreateSuccess(response);
                }

                var dict = payload.Discounts;

                // ===== PHASE 1: Discounts (Aggregate Root) =====
                if (dict.TryGetValue(Constants.RefNames.Discounts, out var discountRequests)
                    && discountRequests != null
                    && discountRequests.Count > 0)
                {
                    foreach (var req in OrderByAction(discountRequests))
                    {
                        var result = await ExecuteRefRequestAsync(
                            Constants.RefNames.Discounts,
                            req.Action,
                            req.Data,
                            cancellationToken);

                        AddResult(response.Results, Constants.RefNames.Discounts, result);
                    }
                }

                // ===== PHASE 2: Other related refs =====
                foreach (var kv in dict)
                {
                    var refName = kv.Key;
                    if (refName == Constants.RefNames.Discounts)
                        continue;

                    var requests = kv.Value;
                    if (requests == null || requests.Count == 0)
                        continue;

                    foreach (var req in OrderByAction(requests))
                    {
                        var result = await ExecuteRefRequestAsync(
                            refName,
                            req.Action,
                            req.Data,
                            cancellationToken);

                        AddResult(response.Results, refName, result);
                    }
                }

                response.SuccessDiscount = response.Results
                    .SelectMany(x => x.Value)
                    .SelectMany(x => x.Items)
                    .All(i => string.IsNullOrEmpty(i.ErrorMessage));

                return HandlerResult<DiscountResponseModel>.CreateSuccess(response);
            }
            catch (Exception ex)
            {
                Log.Error($"Error calling RK7 for SaveDiscount: {ex.Message}", ex);
                return HandlerResult<DiscountResponseModel>.CreateFailure(
                    $"Error executing SaveDiscount: {ex.Message}");
            }
        }

        #region Private Methods

        private static void AddResult(
            IDictionary<string, List<Rk7RefResponseResult>> target,
            string refName,
            Rk7RefResponseResult result)
        {
            if (!target.TryGetValue(refName, out var list) || list == null)
                list = new List<Rk7RefResponseResult>();

            list.Add(result);
            target[refName] = list;
        }

        private static IEnumerable<DiscountRequest> OrderByAction(IEnumerable<DiscountRequest> requests)
        {
            static int Rank(Constants.RefAgentAction action) => action switch
            {
                Constants.RefAgentAction.CREATE => 1,
                Constants.RefAgentAction.UPDATE => 2,
                Constants.RefAgentAction.SOFT_DELETE => 3,
                Constants.RefAgentAction.HARD_DELETE => 4,
                _ => 99
            };

            return requests
                .Where(r => r != null && r.Data != null && r.Data.Length > 0)
                .OrderBy(r => Rank(r.Action));
        }

        private async Task<Rk7RefResponseResult> ExecuteRefRequestAsync(
            string refName,
            Constants.RefAgentAction action,
            Item[] data,
            CancellationToken cancellationToken)
        {
            var resultModel = new Rk7RefResponseResult { Action = action };

            if (data == null || data.Length == 0)
                return resultModel;

            var (ok, errorCode, errorMessage) =
                await SendSetRefDataAsync(refName, action, data, cancellationToken);

            if (!ok)
            {
                foreach (var item in data)
                {
                    resultModel.Items.Add(new Rk7ItemResult
                    {
                        Ident = item?.Ident,
                        GuidString = action == Constants.RefAgentAction.CREATE
                            ? item?.GUIDString
                            : null,
                        ErrorCode = errorCode,
                        ErrorMessage = errorMessage
                    });
                }

                return resultModel;
            }

            if (action == Constants.RefAgentAction.CREATE)
            {
                foreach (var item in data)
                {
                    var ident = await GetObjectIdentByGuidAsync(
                        item?.GUIDString,
                        refName,
                        cancellationToken);

                    resultModel.Items.Add(new Rk7ItemResult
                    {
                        Ident = ident,
                        GuidString = item?.GUIDString
                    });
                }

                return resultModel;
            }

            foreach (var item in data)
            {
                resultModel.Items.Add(new Rk7ItemResult
                {
                    Ident = item?.Ident,
                    GuidString = item?.GUIDString
                });
            }

            return resultModel;
        }

        private async Task<(bool ok, string errorCode, string errorMessage)> SendSetRefDataAsync(
            string refName,
            Constants.RefAgentAction action,
            Item[] data,
            CancellationToken cancellationToken)
        {
            var cmd = new RK7CMD
            {
                CMD = Constants.RK7CMD.SetRefData,
                RefName = refName,
                Items = action == Constants.RefAgentAction.HARD_DELETE ? null : data,
                ItemsToDelete = action == Constants.RefAgentAction.HARD_DELETE ? data : null
            };

            var result = await Rk7Services.SendCommandToRk7ForResultAsync(
                new RK7Query { RK7CMD = cmd });

            if (Utils.IsRk7Success(result))
                return (true, null, null);

            var (code, message) = TryExtractRk7Error(result);
            return (false, code ?? "RK7_ERROR", message ?? "Unknown RK7 error");
        }

        private async Task<string> GetObjectIdentByGuidAsync(
            string guidString,
            string refName,
            CancellationToken cancellationToken)
        {
            if (string.IsNullOrWhiteSpace(guidString))
                return null;

            var cmd = new RK7CMD
            {
                CMD = Constants.RK7CMD.GetRefData,
                RefName = refName,
                PropFilters = new PropFilters
                {
                    Props = new[]
                    {
                        new Prop
                        {
                            Name = Constants.PropNames.GUIDString,
                            Value = guidString
                        }
                    }
                }
            };

            var result = await Rk7Services.SendCommandToRk7ForResultAsync(
                new RK7Query { RK7CMD = cmd });

            return result?.RK7Reference?.Items?.FirstOrDefault()?.Ident;
        }

        private static (string code, string message) TryExtractRk7Error(RK7QueryResult rk7Result)
        {
            return (rk7Result.ErrorText, rk7Result.ErrorText);
        }

        #endregion
    }
}

```

