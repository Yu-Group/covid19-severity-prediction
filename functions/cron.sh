# list of cron jobs currently being run
# crontab -e to edit
# want these all to run once a day at 8am: 0 8 * * * before each command
# ex: 0 8 * * * $(which python3) $REPO_DIR/functions/update_severity_index.py >> ~/cron.log

REPO_DIR=/accounts/projects/vision/chandan/covid19-severity-prediction

# update severity index gsheet + index viz
$(which python3) $REPO_DIR/functions/update_severity_index.py >> ~/cron.log

# update slider plot once a day
$(which python3) $REPO_DIR/functions/update_slider.py $REPO_DIR/data county_pop_centers.csv >> ~/cron.log

# cache IHME preds
# need to run this script: https://github.com/Yu-Group/covid19-severity-prediction/blob/master/predictions/other_modeling/extract_ihme.py

# cache our model preds
# need to run xiao's script

# update model preds plot (like becca plot in paper)
# this script will be coming soon...

# after running all scripts need to push to git