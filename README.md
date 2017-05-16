# CloudFormation Visualizer

##### Summary
This tool will create a Sankey diagram visualizing all CloudFormation stacks within a given AWS account and the cross-stack references in use.  The focus of this tool is to provide a visual linkage between the Exports of a stack and any child stacks that Import those variables.  This will allow for quick identification of dependencies and relationships which are typically difficult to both identify and visualize.

### Setup
1. Install [python3](https://www.python.org/downloads/)
1. Install virtualenv for python.  Install details avaialable at http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/
1. Create a virtualenv (see simple setup below)
1. Have the `awscli` installed and configured with default profile


##### Simple Copy/Paste Initial Setup
After cloning the repo, change into that directory and run:
```
virtualenv myvirtualenvironment
source myvirtualenvironment/bin/activate
pip install -r requirements.txt
```

##### Running the app
The application is comprised of 2 scripts, `get_data_flare.py` and `get_data_sankey.py` that retrieve data from the AWS account via the `awscli` configurations.  By default, the scripts will read from the `default` profile.  This can be overridden by passing a profile name to the script on the command line.  The scripts will generate files that are then read by the webpage that is served in order to display the generated charts.

##### get_data_flare.py
This script will generate a visualization of the stacks in use along with their respective Outputs / Exports.  It does NOT link the stacks and serves primarily as an inventory of output variables.  This is acheived by creating a CSV file that is then used as a data source for http://localhost:8000/index-flare.html (when run locally).

##### get_data_sankey.py
This script creates a Sankey diagram of all stacks and the relationships between the Outputs / Exports of a stack and the downstream stacks that are using those exports.  The Sankey is accessed by following the steps listed below and is hosted on the default 8000 port.

###### Steps
1. Run `./get_data_flare.py <optional-profile-name>`
1. Run `./get_data_sankey.py <optional-profile-name>`
1. Start a simple webserver in the same directory for local display
  1. Python provides a simple HTTP server via `python3 -m http.server` on the command line with a default port of `8000`
1. Navigate to http://localhost:8000 to view the Sankey chart

NOTE: This will not dynamically update the graph with changes in your AWS environment.  You will need to re-run the `get_data_*` scripts to update the graph.

##### Credits
All credit to https://github.com/ACHepcat
Thank you very much!
