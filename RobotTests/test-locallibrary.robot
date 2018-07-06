*** Settings ***
Library     SeleniumLibrary

*** Variables ***
${SERVER}           http://127.0.0.1:8000
${LOGIN_URL}        http://127.0.0.1:8000/accounts/login/
${BROWSER_1}        Chrome
${Browser_2}        Firefox
${SPEED}            .9
${DELAY}            0
@{GENRE}            Mystery     Drama
${DATE}             Get Current Date
${MONTH_TODAY}      July
${DAY_TODAY}        ${6}
${YEAR_TODAY}       2018

*** Test Cases ***
Testing: Login
    Set Selenium Speed  ${SPEED}
    #Open Browser        ${LOGIN_URL}    ${Browser_2}
    Open Browser        ${LOGIN_URL}    ${BROWSER_1}
    Input Text          //*[@id="id_username"]      librarian1
    Input Text          //*[@id="id_password"]      librarian1userpassword
    Click Button        //html/body/div[2]/div/div[3]/form/div[3]/button 
    Capture Page Screenshot

Testing: Displaying Book List
    Click Link          //html/body/div[2]/div/div[1]/nav/ul/li[2]/a

Testing: Book List Pagination
    Click Link          //html/body/div[2]/div/div[3]/ul/li[3]/a
    Click Link          //html/body/div[2]/div/div[3]/ul/li[5]/a
    Click Link          //html/body/div[2]/div/div[3]/ul/li[3]/a

Testing: Adding Book
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

Testing: Updating Book
    Click Element       //html/body/div[2]/div/div[3]/span/a[1]/span
    Input Text          //*[@id="id_title"]         UPDATED New Book Added Through Robot
    Capture Page Screenshot
    Click Button        //html/body/div[2]/div/div[3]/form/input[2]
    Capture Page Screenshot

Testing: Adding Book Instance
    Click Element       //html/body/div[2]/div/div[3]/span/a[3]/span
    Select From List    //*[@id="id_status"]        Available
    Click Button        //html/body/div[2]/div/div[3]/form/input[2]
    Capture Page Screenshot

Testing Deleting Book
    Click Element       //html/body/div[2]/div/div[3]/span/a[2]/span
    Click Button        //html/body/div[2]/div/div[3]/form/input[2]
    Capture Page Screenshot

Testing: Displaying Author List
    Click Link          //html/body/div[2]/div/div[1]/nav/ul/li[3]/a

#Testing: Author List Pagination
    # Only a page is visible

Testing: Adding Author
    Click Link          //html/body/div[2]/div/div[1]/nav/ul/li[4]/ul/li/a
    Input Text          //*[@id="id_first_name"]        New Author First Name Added through Robot
    Input Text          //*[@id="id_last_name"]         New Author Last Name Added Through Robot
    Input Text          //*[@id="id_date_of_birth"]     1996-5-5
    Click Button        //html/body/div[2]/div/div[3]/form/input[2]

Testing: Updating Author Detail
    Click Element       //html/body/div[2]/div/div[3]/a[1]/span
    Input Text          //*[@id="id_first_name"]        Updated Name
    Click Button        //html/body/div[2]/div/div[3]/form/input[2]

Testing: Deleting Author
    Click Element       //html/body/div[2]/div/div[3]/a[2]/span
    Click Button        //html/body/div[2]/div/div[3]/form/input[2]

Testing: Displaying Transactions
    Click Link          //html/body/div[2]/div/div[1]/nav/ul/li[5]/a

Testing: Adding Transactions
    Click Link          //html/body/div[2]/div/div[1]/nav/ul/li[5]/ul/li/a
    Select From List    //*[@id="id_due_date_month"]        ${MONTH_TODAY}
    ${DUE_DAY}         Convert to string                   ${DAY_TODAY + 3}
    Select From List    //*[@id="id_due_date_day"]          ${DUE_DAY}
    Select From List    //*[@id="id_due_date_year"]         ${YEAR_TODAY}
    Select From List    //*[@id="id_borrower"]              user1
    Click Button        //html/body/div[2]/div/div[3]/form/input[2]

Testing: Renewing Borrowed Book
    Click Link          //html/body/div[2]/div/div[3]/table/tbody/tr[2]/td[5]/a
    Input Text          //*[@id="id_renewal_date"]          2018-07-10
    Click Button        //html/body/div[2]/div/div[3]/form/input[2]

Testing: Returning Book
    Click Link          //html/body/div[2]/div/div[3]/table/tbody/tr[2]/td[7]/a
    Input Text          //*[@id="id_remarks"]               In good condition;
    Select From List    //*[@id="id_date_returned_month"]   ${MONTH_TODAY}
    Select From List    //*[@id="id_date_returned_day"]     Convert to string       ${DAY_TODAY}
    Select From List    //*[@id="id_date_returned_year"]    Convert to string       ${YEAR_TODAY}
    Click Button        //html/body/div[2]/div/div[3]/form/input[2]

