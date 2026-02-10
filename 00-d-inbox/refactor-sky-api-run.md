## sửa theo  n-tier layered architecture
## flow
-> step1.Libraries
Core=>Data=>Service
-> step2.Presentation
Web.API
## tree 
``` refactor
Libraries
├── Core
│   └── Domain
│       └── RK7
│           ├── Item.cs
│           ├── Prop.cs
│           ├── PropFilter.cs
│           ├── PropFilters.cs
│           ├── RK7CMD.cs
│           ├── RK7Query.cs
│           ├── RK7QueryResult.cs
│           ├── RK7Reference.cs
│           └── RK7RefList.cs
│
└── Service
    └── Apps
    │  └── AppHelpers.cs
    Discounts
    ├── Abstractions
    │   ├── IBackgroundJobHandler.cs
    │   ├── IEcomTrackSyncRequest.cs
    │   ├── ISkyCRMDiscountIntegrationCommand.cs
    │   └── SkyCRMDiscountReqBase.cs
    │
    ├── Background
    │   ├── BackgroundTaskQueue.cs
    │   ├── BackgroundWorker.cs
    │   ├── IBackgroundTaskQueue.cs
    │   └── ShareDiscountIntegrationMapper.cs
    │
    ├── External
    │   └── Clients
    │       ├── ExternalApiClientBase.cs
    │       ├── IRefAgentApiClient.cs
    │       ├── IRK7ApiClient.cs
    │       ├── RefAgentApiClient.cs
    │       └── RK7ApiClient.cs
    │
    ├── Handlers
    │   └── AutoDiscountJobHandler.cs
    │
    ├── Integration
    │   ├── RefAgentDiscountIntegrationService.cs
    │   ├── RK7DiscountIntegrationService.cs
    │   └── SkyTransferDiscountIntegrationService.cs
    │
    └── Models
        ├── Refagent
        │   ├── Item.cs
        │   ├── RefAgentDiscountIntegrationCommand.cs
        │   ├── RefAgentDiscountIntegrationMapper.cs
        │   └── RefAgentDiscountIntegrationResponse.cs
        │
        ├── RK7
        │   ├── RK7DiscountIntegrationItemDto.cs
        │   ├── RK7DiscountItemIntegrationMapper.cs
        │   └── RK7DiscountJobResultIntegrationResponse.cs
        │
        ├── EcomTrackSyncRequest.cs
        ├── IBackgroundJob.cs
        ├── ISkyCRMDiscountIntegrationCommand.cs
        ├── ManualDiscountJob.cs
        ├── SkyCRMDiscountCreateOrUpdateIntegrationCommand.cs
        ├── SkyCRMDiscountDeleteIntegrationCommand.cs
        ├── SkyCRMDiscountIntegrationCommand.cs
        ├── SkyCRMDiscountIntegrationCommandResponse.cs
        ├── SkyCRMDiscountJob.cs
        └── SkyCRMDiscountValid.cs

└── Web.Api
    ├── Controllers
    │   └── Discounts
    │       └── SkyTransferDiscountController.cs
    │
    └── Services
        └── Discounts
            └── Handlers
                └── ManualDiscountJobHandler.cs
```




