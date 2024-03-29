![spice2jira](media/application_preview.png)

# Spice2JIRA
A small python tool for preparing a migration from Spiceworks to Jira Service Management.

## Summary
Spiceworks used to be a free, self-hosted ticketing system.  Their current system has left their core customer base with the choice of leaving their self-hosted solution with the option of using an unsupported solution or be migrated on to their paid, cloud-hosted solution.

Spiceworks has been harvesting user submitted data for a very long time.  They have also been using self-hosted resources to present advertisements with the processsing power of their customers, to serve advertisements on internal tickets as a revenue model.  Since their change to the cloud-based SaaS model, many users have decided their product offering isn't what it's cracked up to be. Those end-users have decided (to their own detriment) that JIRA Service Management is a much better solution for the price and feature set.  If your internal IT Services team is less than 5 users, this might be a tool for you for free.  If your IT Services team is larger than that, this is still a tool for you. You just might need to put more work into scrubbing the data (depending how long you've been using spiceworks).

Each button to press in the application is a step for an administrator to check and scrub their data to make sure it's ready for an import to JIRA Serivce Management... which also used to be called JIRA Service Desk. For how much Atlassian has issues, it's probably not as bad as Spiceworks is.

This methodology will help IT Admins prepare for their eventual move to a tool that is used by the wider technology industry. For better or for worse.

## Step 1 - Select Your JSON File
![Step 1 - Import JSON](media/application_preview-step-1.png)

This is place where you're going to be able to select the JSON file where all of your ticket and user data has been exported to.  Please keep in mind at this point, this application is only validating this is correct JSON, and not the format that is needed for the rest of the steps in this process.

## Step 2 - Select the Output Directory for CSV Files
![Step 2 - Choose Output Directory](media/application_preview-step-2.png)

The directory chosen here is where `users.csv` and `tickets.csv` going to be created. Once the csv files are created, headers are added to the csv file. This will be the working directory for the rest of the prepared import file to JIRA Service Management.

## Step 3 - Create the Spiceworks User Table
![Step 3 - Create User Table](media/application_preview-step-3.png)

Click the `Create User Table` button to populate the `users.csv` file.  This will sort through the exported json file and fill the csv file with users data including name, role, email address, and the user ID assigned via Spiceworks.

Be sure to manually go through this file to make any desired changes to the users before moving on to the next step.

## Step 4 - Create the Spiceworks Ticket Table
![Step 4 - Create Ticket Table](media/application_preview-step-4.png)

Click the `Create Ticket Table` button to populate the `tickets.csv` file.  This will sort through the exported json file and filel the csv file with ticket data including userid, created/closed times, ticket status, summary, description and comments.

This will be a good opportuntiy to manually go through the `tickets.csv` file to manually to see if there is anything that looks incorrectly formatted in the file.

## Step 5 - Assign User ID Numbers to E-Mail Addresses
![Step 5 - Assign User IDs](media/application_preview-step-5.png)

Before the `tickets.csv` file can be imported to JIRA, we'll need to changed all of the numeric user IDs in spiceworks to the email address associated with it.  This will go through each line of `tickets.csv`, get the assignee's ID number and the requestor's ID number and perform lookups of those numbers in `users.csv` and grab the associated email.

It will then replace those user IDs with the approriate email address in the `tickets.csv` file.

## Step 6 - Merge Description & Comment Columns
![Step 6 - Merge Description and Comment Columns](media/application_preview-step-6.png)

JIRA doesn't officially support importing comments. The best, cheapest, and quickest route is importing all comments into the ticket description directly from the spiceworks data.

At this point, we're merging the Description, and Comments column together.  This is another great opportunity for you to look over your entire `tickets.csv` file. Make sure that this formatting is correct (manually).

## Step 7 - Interpret Unicode Escape Characters
![Step 7 - Interpret Escape Chars.](media/application_preview-step-7.png)

JIRA Service Management doesn't interpret Unicode Escape Characters.  That means not every ticket and relevant information can be stored on one line.  By clicking this button, all unicode escape characters are interpreted in a very messy-looking (but importable) CSV file.

Congrats!  Now you're ready for an import through JIRA's import wizard!
