# list of cron jobs currently being run
# crontab -e to edit
# want these all to run once a day at 8am: 0 8 * * * before each command
# ex: 0 8 * * * /path/to/cron.sh

REPO_DIR=/home/ubuntu/new_uploader
LOG_FILE=$REPO_DIR/functions/update_test.log
PATH=/home/ubuntu/anaconda3/bin/:$PATH
export PATH
rm $LOG_FILE


cd $REPO_DIR
git pull origin master
# update usafacts and nytimes data
cd $REPO_DIR/data/county_level/raw/nytimes_infections
$(which python3) download.py >> $LOG_FILE
cd $REPO_DIR/data/county_level/processed/nytimes_infections
$(which python3) clean.py >> $LOG_FILE

cd $REPO_DIR/data/county_level/raw/usafacts_infections
$(which python3) download.py >> $LOG_FILE
cd $REPO_DIR/data/county_level/processed/usafacts_infections
$(which python3) clean.py >> $LOG_FILE

# push to git
git add .

# commit to git
git commit -am "update usafacts and nytimes data"

# push to origin
git push --quiet https://$GIT_USERNAME:$GIT_PASSWORD@github.com/Yu-Group/covid19-severity-prediction.git 

# update severity index gsheet + index viz
$(which python3) $REPO_DIR/functions/update_severity_index.py >> $LOG_FILE

# update map slider plot once a day
$(which python3) $REPO_DIR/functions/update_map_with_slider.py >> $LOG_FILE

# update model preds plot
$(which python3) $REPO_DIR/functions/update_predictions_plot.py >> $LOG_FILE

# cache IHME preds
# $(which python3) $REPO_DIR/functions/update_ihme.py >> $LOG_FILE

# after running all scripts need to push to git
cd $REPO_DIR

# pull from origin
git pull origin master
git add .

# commit to git
git commit -am "daily update"

# push to origin
git push --quiet https://$GIT_USERNAME:$GIT_PASSWORD@github.com/Yu-Group/covid19-severity-prediction.git 
