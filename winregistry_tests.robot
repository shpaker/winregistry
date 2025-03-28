*** Variables ***
${ SUITE_KEY_NAME }       HKLM\\SOFTWARE\\_ROBOT_TESTS_
${ SHORT_CASE_KEY_NAME }  _CASE_KEY_
${ CASE_KEY_NAME }        ${ SUITE_KEY_NAME }\\${ SHORT_CASE_KEY_NAME }
${ VALUE_NAME }           some_testing_value
${ NESTED_KEY_PATH }      ${ SUITE_KEY_NAME }\\FOO\\BAR\\BAZ

*** Settings ***
Library         Collections
Library         winregistry.robot
Suite Setup     Create Registry Key  ${ SUITE_KEY_NAME }
Suite Teardown  Delete Registry Key  ${ SUITE_KEY_NAME }   recursive=True

*** Test Cases ***
CREATE REGISTRY KEY
    [Teardown]  Delete Registry Key     ${ CASE_KEY_NAME }
    Registry Key Should Not Exist   ${ CASE_KEY_NAME }
    Create Registry Key             ${ CASE_KEY_NAME }
    Registry Key Should Exist       ${ CASE_KEY_NAME }

VERIFY REGISTRY KEY IN PARENT
    [Teardown]  Delete Registry Key     ${ CASE_KEY_NAME }
    Create Registry Key             ${ CASE_KEY_NAME }
    ${ items } =    Get Registry Key Sub Keys   ${ SUITE_KEY_NAME }
    List Should Contain Value       ${ items }  ${ SHORT_CASE_KEY_NAME }

CREATE EMPTY REGISTRY VALUE
    [Setup]     Create Registry Key         ${ CASE_KEY_NAME }
    [Teardown]  Delete Registry Key         ${ CASE_KEY_NAME }
    Create Registry Value                   ${ CASE_KEY_NAME }  ${ VALUE_NAME }  SZ
    ${ value } =    Read Registry Value     ${ CASE_KEY_NAME }  ${ VALUE_NAME }
    Should Be Equal     ${ value.data }     ${ EMPTY }

SET AND READ REGISTRY VALUE
    [Setup]     Create Registry Key         ${ CASE_KEY_NAME }
    [Teardown]  Delete Registry Key         ${ CASE_KEY_NAME }
    Create Registry Value                   ${ CASE_KEY_NAME }  ${ VALUE_NAME }  SZ
    Set Registry Value                      ${ CASE_KEY_NAME }  ${ VALUE_NAME }  Remove me!
    ${ value } =    Read Registry Value     ${ CASE_KEY_NAME }  ${ VALUE_NAME }
    Should Be Equal     ${ value.data }     Remove me!

DELETE REGISTRY VALUE
    [Setup]     Create Registry Key         ${ CASE_KEY_NAME }
    [Teardown]  Delete Registry Key         ${ CASE_KEY_NAME }
    Create Registry Value                   ${ CASE_KEY_NAME }  ${ VALUE_NAME }  SZ
    Set Registry Value                      ${ CASE_KEY_NAME }  ${ VALUE_NAME }  Remove me!
    Delete Registry Value                   ${ CASE_KEY_NAME }  ${ VALUE_NAME }
    ${ items } =    Get Registry Key Values Names   ${ CASE_KEY_NAME }
    List Should Not Contain Value           ${ items }          ${ VALUE_NAME }

CREATE NESTED REGISTRY KEYS
    [Teardown]  Delete Registry Key     ${ NESTED_KEY_PATH }   recursive=True
    Registry Key Should Not Exist   ${ NESTED_KEY_PATH }
    Create Registry Key             ${ NESTED_KEY_PATH }
    Registry Key Should Exist       ${ NESTED_KEY_PATH }

DELETE NESTED REGISTRY KEYS RECURSIVELY
    [Setup]     Create Registry Key     ${ NESTED_KEY_PATH }
    Registry Key Should Exist       ${ NESTED_KEY_PATH }
    Delete Registry Key             ${ NESTED_KEY_PATH }   recursive=True
    Registry Key Should Not Exist   ${ NESTED_KEY_PATH }

VERIFY REGISTRY KEY DOES NOT EXIST
    Registry Key Should Not Exist   ${ CASE_KEY_NAME }
    ${ items } =    Get Registry Key Sub Keys   ${ SUITE_KEY_NAME }
    List Should Not Contain Value   ${ items }  ${ SHORT_CASE_KEY_NAME }

VERIFY REGISTRY VALUE DOES NOT EXIST
    [Setup]     Create Registry Key         ${ CASE_KEY_NAME }
    [Teardown]  Delete Registry Key         ${ CASE_KEY_NAME }
    ${ items } =    Get Registry Key Values Names   ${ CASE_KEY_NAME }
    List Should Not Contain Value           ${ items }          ${ VALUE_NAME }
    Registry Value Should Not Exist         ${ CASE_KEY_NAME }  ${ VALUE_NAME }
