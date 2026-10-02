# hdd-validation-backend-service

A small Python backend that will read a hard drive test log and return PASS or FAIL, the highest temperature, and any faults with their line numbers.

Status: work in progress. This is a learning project on synthetic logs with an invented format. It is not connected to any real tester or company data.

## The problem

Test rigs write long log files after every run. Engineers open them one by one and search for errors by hand, which is slow and easy to get wrong. This project turns that into a single API call.

The scenario above is illustrative, not real company data.
