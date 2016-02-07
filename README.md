# powerline-testsuite
Simple python class for testing the Powerline Server API

## powerline.py
Used to directly issue http requests to the Powerline API. This will handle all HTTP request types and
session info via login/facebook login. 

_Login also assumes you already have a login username/password._ 

# Building Tests

Currently, only user tests are available. These tests are ran against the Powerline API as a standard 
user. Once we unify our security provider, managers, leaders and representatives will be using the same
interface. 

For now, all unit tests should extend `powerlineusertest.PowerlineUserTests`

## User Tests

All user tests are for testing the capabilities of a standard user

Here is a basic example:

```
import unittest
import powerlineusertests

class NewUserTest(powerlineusertest.PowerlineUserTests):

    def test_sometest(self):
        compare = ['a','b']
        resp = self.api.get('/fake/endpoint')
        d = resp.json()
        self.assertEqual(d , compare)

if __name__ == "__main__":
    unittest.main()
```

## Manager/Leader Tests

Will need to be built after we unify our security providers

# Running Tests

You can also run a test standalone:

` python -m unittest -v some_test.py`

Or run all tests in the dir:

` python -m unittest discover -s <dir> -p "*_test.py"`

