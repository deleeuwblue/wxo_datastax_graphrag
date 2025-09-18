# GraphRAG with watsonx oOrchestrate with Datastax

This repository shows how to use watsonx Orchestrate with Datastax database, to provide GraphRAG capabilities.

## Setup

To run this sample you need:

- a container runtime
- VSCode with the Dev Containers and Jupyter Notebook features added
- a Kaggle account to access the test data
- either IBM software catalog access and watsonx.ai or watsonx Orchestrate

### Container Runtime

The watsonx Orchestrate Agent Development Kit (ADK) has the watsonx Orchestrate Developer Edition included.  This uses a container runtime to run locally on your system, with AI inferencing being done remotely using watsonx Orchestrate or watsonx.ai.  The setup of the is covered in the [ADK Documentation](https://developer.watson-orchestrate.ibm.com/developer_edition/wxOde_setup#configuring-container-manager).

!!!TODO
  add blog URL
  
This repository also supports the VS Code Dev Containers feature to run the watsonx Orchestrate Developer Edition.  Details of the setup are covered in [this blog](xxx)


!!!TODO
  explain:
  - getting watsonx Orchestrate or watsonx.ai for ADK env vars
  - getting AstraDB instance and credentials
  - getting Kaggle move review data and adding to data directory
  - setting up env file

### VSCode setup

!!!TODO
  explain:
  - devContainers setup (docker/colima/podman?)
  - Jupyter within VSCode
  - Launching ADK and loading sample agent/tools


### Running sample

!!!TODO
  explain:
  - run notebook to populate AstraDB database with movie data
  - Launch ADK and switch to agent
  - enter question
