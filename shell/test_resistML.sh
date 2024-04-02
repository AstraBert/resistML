echo "TEST RESULTS" > test/tests_resistML.results

for i in {0..9}
do
    python3 scripts/resistML_predict.py \
        -i test/testfiles/test_${i}.csv \
        -c resistML.joblib >> test/tests_resistML.results
done