*** Variables ***
${ SUITE_KEY_NAME }       HKLM\\SOFTWARE\\_ROBOT_TESTS_
${ SHORT_CASE_KEY_NAME }  _CASE_KEY_
${ CASE_KEY_NAME }        ${ SUITE_KEY_NAME }\\${ SHORT_CASE_KEY_NAME }
${ VALUE_NAME }           some_testing_value

*** Settings ***
Library         Collections
Library         winregistry.robot
Suite Setup     Create Registry Key  ${ SUITE_KEY_NAME }
Suite Teardown  Delete Registry Key  ${ SUITE_KEY_NAME }   recursive=True

*** Test Cases ***
TEST REGISTRY KEYS
    [Teardown]  Delete Registry Key     ${ CASE_KEY_NAME }

    ${ items } =    Get Registry Key Sub Keys   ${ SUITE_KEY_NAME }
    List Should Not Contain Value   ${ items }  ${ SHORT_CASE_KEY_NAME }
    Registry Key Should Not Exist   ${ CASE_KEY_NAME }
    Create Registry Key             ${ CASE_KEY_NAME }
    Registry Key Should Exist       ${ CASE_KEY_NAME }
    ${ items } =    Get Registry Key Sub Keys   ${ SUITE_KEY_NAME }
    List Should Contain Value       ${ items }  ${ SHORT_CASE_KEY_NAME }


TEST REGISTRY VALUES
    [Setup]     Create Registry Key         ${ CASE_KEY_NAME }
    [Teardown]  Delete Registry Key         ${ CASE_KEY_NAME }

    ${ items } =    Get Registry Key Values Names   ${ CASE_KEY_NAME }
    List Should Not Contain Value           ${ items }          ${ VALUE_NAME }
    Registry Value Should Not Exist         ${ CASE_KEY_NAME }  ${ VALUE_NAME }
    Create Registry Value                   ${ CASE_KEY_NAME }  ${ VALUE_NAME }  SZ
    Registry Value Should Exist             ${ CASE_KEY_NAME }  ${ VALUE_NAME }
    ${ items } =    Get Registry Key Values Names   ${ CASE_KEY_NAME }
    List Should Contain Value               ${ items }          ${ VALUE_NAME }
    ${ value } =    Read Registry Value     ${ CASE_KEY_NAME }  ${ VALUE_NAME }
    Should Be Equal     ${ value.data }     ${ EMPTY }
    Set Registry Value                      ${ CASE_KEY_NAME }  ${ VALUE_NAME }  Remove me!
    ${ value } =    Read Registry Value     ${ CASE_KEY_NAME }  ${ VALUE_NAME }
    Should Be Equal     ${ value.data }     Remove me!
    Delete Registry Value                   ${ CASE_KEY_NAME }  ${ VALUE_NAME }

TEST RECURSIVELY DELETE KEY
    Registry Key Should Not Exist   HKLM\\SOFTWARE\\_ROBOT_TESTS_\\FOO
    Create Registry Key             HKLM\\SOFTWARE\\_ROBOT_TESTS_\\FOO\\BAR\\BAZ
    Registry Key Should Exist       HKLM\\SOFTWARE\\_ROBOT_TESTS_\\FOO
    Delete Registry Key             HKLM\\SOFTWARE\\_ROBOT_TESTS_\\FOO   recursive=True
    Registry Key Should Not Exist   HKLM\\SOFTWARE\\_ROBOT_TESTS_\\FOO
