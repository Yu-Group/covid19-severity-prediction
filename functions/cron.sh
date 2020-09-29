# list of cron jobs currently being run
# crontab -e to edit
# want these all to run once a day at 8am: 0 8 * * * before each command
# ex: 0 8 * * * /path/to/cron.sh

REPO_DIR=/home/ubuntu/new_uploader
DASHBOARD_DIR=/home/ubuntu/covid19-dashboard
LOG_FILE=$REPO_DIR/functions/update_test.log
PATH=/home/ubuntu/anaconda3/bin/:$PATH
export PATH
rm $LOG_FILE

################# update data #####################
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




################# update visualizations #####################
# update severity index gsheet + index viz
$(which python3) $REPO_DIR/functions/update_severity_index.py >> $LOG_FILE

# update map slider plot once a day
$(which python3) $REPO_DIR/functions/update_map_with_slider.py >> $LOG_FILE

# update model preds plot
$(which python3) $REPO_DIR/functions/update_predictions_plot.py >> $LOG_FILE

# update the search map
$(which python3) $REPO_DIR/functions/data_engineering.py >> $LOG_FILE
$(which python3) $REPO_DIR/functions/update_search.py >> $LOG_FILE

# move the search map to other repo
cp $REPO_DIR/results/All_counties/* $DASHBOARD_DIR/results/All_counties
cp $REPO_DIR/functions/update_search.json $DASHBOARD_DIR/functions
cp -r $REPO_DIR/results/* $DASHBOARD_DIR/results
# cp $REPO_DIR/results/search.html $DASHBOARD_DIR/results/
# cache IHME preds
# $(which python3) $REPO_DIR/functions/update_ihme.py >> $LOG_FILE

# push the dashboard repo
cd DASHBOARD_DIR=/home/ubuntu/covid19-dashboard
git pull origin master # pull from origin
git add .
git commit -am "daily update" # commit to git
git push --quiet https://$GIT_USERNAME:$GIT_PASSWORD@github.com/Yu-Group/covid19-dashboard.git # push to origin


# after running all scripts need to push to git
cd $REPO_DIR
git pull origin master # pull from origin
git add .
git commit -am "daily update" # commit to git

# push to origin
git push --quiet https://$GIT_USERNAME:$GIT_PASSWORD@github.com/Yu-Group/covid19-dashboard.git 
