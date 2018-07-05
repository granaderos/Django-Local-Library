*** Settings ***
Library     SeleniumLibrary

*** Variables ***
${SERVER}       http://127.0.0.1:8000
${LOGIN_URL}    http://127.0.0.1:8000/accounts/login/
${BROWSER}      Chrome
${SPEED}        .9
${DELAY}        0
@{GENRE}        Mystery     Drama

*** Test Cases ***
Testing Login
    Set Selenium Speed  ${SPEED}
    Open Browser        ${LOGIN_URL}    ${BROWSER}
    Capture Page Screenshot
    Input Text          //*[@id="id_username"]      librarian1
    Input Text          //*[@id="id_password"]      librarian1userpassword
    Click Button        //html/body/div[2]/div/div[3]/form/div[3]/input[1] 
    Capture Page Screenshot

Testing Adding Book Feature
    Click Link          //html/body/div[2]/div/div[1]/nav/ul/ul/li/a
    Input Text          //*[@id="id_title"]         New Book Added Through Robot
    Select From List    //*[@id="id_author"]        op, po
    Input Text          //*[@id="id_summary"]       New Book Added Through Robot summary. New Book Added Through Robot summary. 
    Input Text          //*[@id="id_isbn"]          45652
    Input Text          //*[@id="id_imprint"]       Random input for id_imprint
    Select From List    //*[@id="id_genre"]         @{GENRE}
    Select From List    //*[@id="id_language"]      Filipino
    #Input Text          //*[@id="id_copies"]        d1
    Capture Page Screenshot
    Click Button        //html/body/div[2]/div/div[3]/form/input[2]
    Capture Page Screenshot

Testing Updating Book
    Click Element       //html/body/div[2]/div/div[3]/span/a[1]/span
    Input Text          //*[@id="id_title"]         UPDATED New Book Added Through Robot
    Capture Page Screenshot
    Click Button        //html/body/div[2]/div/div[3]/form/input[2]
    Capture Page Screenshot

Testing Adding Book Instance
    Click Element       //html/body/div[2]/div/div[3]/span/a[3]/span
    Select From List    //*[@id="id_status"]        Available
    Click Button        //html/body/div[2]/div/div[3]/form/input[2]
    Capture Page Screenshot