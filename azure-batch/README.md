# How to use the Azure Batch for VideoMultiAgent

Using Azure Batch, you can run the VideoMultiAgent more speedily.

![azure_batch_nodes](../docs/azure_batch_nodes.png)


## 📝 Evaluation Time

- The evaluation time of EgoSchema fullset is about 1 hour with 280 instances.
- The evaluation time of EgoSchema subset is about 6 minutes with 280 instances.


## 🚀Execute the script

- ### Step1 : Set the environment variables in run_evaluation.py

    - Please set the environment variables in the run_evaluation.py file.

        [`Click Here to jump to the code`](https://github.com/PanasonicConnect/VideoMultiAgents/blob/main/azure-batch/run_evaluation.py#L18-L45)


- ### Step2 : Run the script

    - MultiAgent will work on the Azure Batch environment.

        `python3 run_evaluation.py`

- ### Step3 : Caluculate the metrics

    - Get the metrics from the cosmos db and calculate the metrics.

        `python3 run_collect_eval_metrics.py`

## 🚀Run the script to automatically scale the Azure Batch pool size.

- By running the script below, the pool size in Azure Batch is automatically adjusted according to the number of tasks that need to be processed.

    `python3 auto_scale_controller.py`
