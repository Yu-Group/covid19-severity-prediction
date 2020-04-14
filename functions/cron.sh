# list of cron jobs currently being run
# crontab -e to edit
# want these all to run once a day at 8am: 0 8 * * * before each command
# ex: 0 8 * * * /path/to/cron.sh

REPO_DIR=/home/ubuntu/uploader
LOG_FILE=$REPO_DIR/functions/update_test.log
PATH=/home/ubuntu/anaconda3/bin/:$PATH
export PATH
rm $LOG_FILE

# update usafacts and nytimes date
$REPO_DIR/data/nytimes/update_data.sh
$REPO_DIR/data/usafacts/update_data.sh

# update severity index gsheet + index viz
$(which python3) $REPO_DIR/functions/update_severity_index.py >> $LOG_FILE

# update map slider plot once a day
$(which python3) $REPO_DIR/functions/update_map_with_slider.py >> $LOG_FILE

# update model preds plot
$(which python3) $REPO_DIR/functions/update_predictions_plot.py >> $LOG_FILE

# cache our model preds (in gdoc)
$(which python3) $REPO_DIR/functions/update_county_preds.py >> $LOG_FILE

# cache IHME preds
$(which python3) $REPO_DIR/functions/update_ihme.py >> $LOG_FILE

# after running all scripts need to push to git
$REPO_DIR/data/push_to_git.sh
