
*********************** Mental Anguish Trivia Application ***********************

PURPOSE: The purpose of this application is to provide a trivia system that users can interact with. Questions are
stored in a file and are loaded/saved from/to there. Users can also manage questions by adding one, deleting one, or
editing one (!!!CHANGING THE QUESTION TEXT CONSTITUTES ADDING A NEW QUESTION NOT EDITING IT. EDITING REFERS TO SELECTING
THE QUESTION TEXT AND CHANGING IT DEPENDENCIES!!!). Additionally user can search for a specific question by utilizing
a textbox

++++++ TAKING A QUIZ ++++++
Press the Take Quiz area in the menu bar
A random question will appear
Select the answer you think is right
Press the submit button
Feedback will appear telling you if you got the question right
Click the Next button to go to the next question
On the last question, instead of Next there will be a Finish button
Clicking on the Finish button will lead the user to an end screen where their total points and number of correct
    questions will be displayed


++++++ ADDING QUESTIONS ++++++
Go to the Manage Question section in the menu bar
On the right hand side, enter in all the information you want as a question
Once completed, click the OK button to add question to listbox and application
To prevent faulty questions, the application might show a messagebox error illustrating what fields need to be fixed.
    Fix fields and then press OK button again
To clear out all the fields press the Cancel button


++++++ EDITING QUESTIONS ++++++
Go to the Manage Questions section in the menu bar
In the listbox, double click a question to edit
The field on the right hand side will populate with all the dependencies of that question
Once completed click the OK button to add question
The old question will be deleted and replaced with the new one
!!! IMPORTANT: Changing the question text itself does not constitute editing a question. That would be adding a new
    question. Therefore, the added new question will appear in the listbox and the user will need to delete the old
    question

++++++ DELETING QUESTIONS ++++++
Go to the Manage Questions section in the menu bar
In the listbox, triple click on a question to delete
A message will appear asking if you are sure that is the question you want to delete
Clicking yes will delete the question from the listbox and application entirely

++++++ SEARCHING QUESTIONS ++++++
Go to the Search Questions section in the menu bar
Type in the question you are looking for in the textbox below the listbox and then press the search button
If you did not get the results you wanted, be more specific in the textbox and try again
To show all questions, clear the textbox and press the search button

++++++ EXIT APPLICATION ++++++
To exit application either press Exit in the menu bar or the X in the top right-hand corner
All data will be saved before application exits

------ SAVING DATA ------
Data will automatically be saved before the application is exited
The data will be stored in a JSON format and saved to a JSON file

------ LOADING DATA ------
Data will automatically be loaded in the application when the application starts
The data is loaded from a JSON file
Afterwards, it will the be created into a Question Object and stored in a list of other objects
