# timeline
- sketch viết tay
- sketch logic
- code mẫu
# sketch logic

## sketch viết tay
- phase 1: kiểm tra đầu vào và kiểm duyệt thông tin hợp lệ (entry và guard)
	-> kiểm tra payload và request (đưa cái gì cho ai ở đâu)
- phase 2: lấy danh sách yêu cầu, sắp xếp theo thứ tự và ghi nhận kết quả mong đợi
	-> kiểm tra trong payload có refname = discounts
	-> lấy danh sách request của discounts sắp xếp theo (create, update, soft_delete, hard_delete)

## tổng thể handler (bức tranh lớn)

- loại handler: command-driven batch handler
- phạm vi: sync discount + các ref liên quan
- chiến lược:

  * aggregate root chạy trước
  * ref phụ chạy sau
  * mọi thứ có thứ tự, không đoán mò
  * success/fail quyết ở mức job

---

## phase 0: entry & guard

- handler được gọi với:

  * request (setrefdata)
  * payload (discountrequestmodel)
- khởi tạo response:

  * synctaskid
- nếu payload rỗng hoặc không có discounts:

  * successdiscount = false
  * return sớm
- mục tiêu:

  * tránh chạy job vô nghĩa
  * fail sớm, fail rõ

---

## phase 1: aggregate root – discounts

- kiểm tra trong payload có refname = discounts không
- nếu có:

  * lấy danh sách request của discounts
  * sắp xếp theo action:

    * create
    * update
    * soft_delete
    * hard_delete
- với mỗi request:

  * gọi execute ref request
  * push result vào response.results["discounts"]

tư duy cốt lõi:

- discounts sinh ra ident
- mọi ref khác phụ thuộc ident này
- chạy sau là gãy chuỗi

---

## phase 2: related refs (phụ thuộc discounts)

- duyệt toàn bộ dictionary payload
- bỏ qua refname = discounts
- với mỗi refname còn lại:

  * nếu có request:

    * sắp xếp theo action (giống phase 1)
    * execute từng batch
    * add result theo refname

đặc điểm:

- không song song
- không retry phức tạp
- ưu tiên trace + ổn định

---

## phase 3: execute một batch (execute ref request)

### step 3.1: khởi tạo result model

- tạo rk7refresponseresult
- gắn action hiện tại

---

### step 3.2: guard data

- nếu data null hoặc empty:

  * return result rỗng
  * coi như batch này ok

---

### step 3.3: gửi command xuống rk7

- build rk7cmd:

  * setrefdata
  * hard_delete → itemstodelete
  * còn lại → items
- send qua rk7services

---

### step 3.4: rk7 fail

- parse error
- với mỗi item trong batch:

  * mark error
  * gắn errorcode + errormessage
- return result
- không xử lý lẻ từng item

triết lý:

- batch fail thì fail hết
- tránh trạng thái nửa đúng nửa sai

---

### step 3.5: rk7 success

- phân nhánh theo action:

- create:

  * với mỗi item:

    * query lại rk7 bằng guidstring
    * lấy ident mới
    * add vào result

- update:

  * giữ ident + guid
  * add vào result

- delete:

  * chỉ giữ ident
  * guid = null

---

## phase 4: tổng hợp kết quả job

- duyệt toàn bộ response.results
- flatten toàn bộ item result
- kiểm tra:

  * có item nào có errormessage không?
- nếu không:

  * successdiscount = true
- nếu có:

  * successdiscount = false

lưu ý:

- success ở mức job
- không phải “có vài cái ok là ok”

---

## phase 5: exception boundary

- nếu có exception ngoài dự kiến:

  * log error
  * trả handler failure
- không nuốt lỗi
- không trả success giả

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

