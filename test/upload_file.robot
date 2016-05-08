*** Settings ***
Documentation     Test file uploading
Library           Selenium2Library
Suite Setup       Setup test suite
Suite Teardown    Close browser
Test Setup        Go to  ${url_home}

*** Variables ***
${browser}           Chrome
${url_base}          http://127.0.0.1:8000
${url_home}          ${url_base}/

*** Test Cases ***
Upload valid file
    Given a valid srt file
    Then page should contain toolbar
    And page should contain up to 10 subtitles

Upload invalid file
    Given an invalid srt file
    Then page should contain disabled toolbar
    And page should contain error

*** Keywords ***
Setup test suite
    Set selenium speed    .5
    Open browser          ${url_home}  ${browser}

A valid srt file
    Choose file    id=btn-upload_srt  %{PWD}/test/data/srt-2_subtitles.srt

An invalid srt file
    Choose file    id=btn-upload_srt  %{PWD}/test/data/srt-invalid_identifier.srt

Page should contain toolbar
    Wait until element is visible    section-toolbar
    :FOR  ${field id}  IN  btn-apply_filter  btn-download  btn-upload-visible
    \    ${disabled} =                    get element attribute  ${field id}@disabled
    \    Should be true                   ${disabled} == None

Page should contain disabled toolbar
    Wait until element is visible    section-toolbar
    :FOR  ${field id}  IN  btn-apply_filter  btn-download
    \    ${disabled} =                    get element attribute  ${field id}@disabled
    \    Should be true                   '${disabled}' == 'true'
    ${disabled} =                    get element attribute  btn-upload-visible@disabled
    Should be true                   ${disabled} == None

Page should contain up to ${count} subtitles
    ${count_actual} =    Get Matching Xpath Count  //section[@id='section-workspace']/ul/li
    Should be true       ${count_actual} <= ${count}

Page should contain error
    Element should contain  xpath=//div[@class='error']  The uploaded file is not a valid srt file
