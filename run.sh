hadoop jar /u/hadoop/karavanic/hadoop-2.5.1/share/hadoop/tools/lib/hadoop-streaming-2.5.1.jar \
-file mapper.py    -mapper mapper.py \
-file reducer.py   -reducer reducer.py \
-input /twitter/08/01/* -output /user/**username**/demo-out
