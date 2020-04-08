# list of cron jobs currently being run
# crontab -e to edit
# want these all to run once a day at 8am: 0 8 * * * before each command
# ex: 0 8 * * * $(which python3) $REPO_DIR/functions/update_severity_index.py >> ~/cron.log

REPO_DIR=/home/ubuntu/uploader

# update usafacts and nytimes date

$REPO_DIR/data/nytimes/update_data.sh
$REPO_DIR/data/usafacts/update_data.sh

# update severity index gsheet + index viz
$(which python3) $REPO_DIR/functions/update_severity_index.py >> ~/cron.log

# update slider plot once a day
$(which python3) $REPO_DIR/functions/update_slider.py >> ~/cron.log

# update model preds plot
$(which python3) $REPO_DIR/functions/update_modeling_results.py >> ~/cron.log

# cache IHME preds
# need to run this script: https://github.com/Yu-Group/covid19-severity-prediction/blob/master/predictions/other_modeling/extract_ihme.py

# cache our model preds
# need to run xiao's script

# after running all scripts need to push to git
