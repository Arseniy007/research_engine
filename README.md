# Research Engine (R.E.)
## My CS50 Final Project

R.E. – is a platform build specifically for those, who deal with writing academic (and nonacademic texts alike) on a daily basis. Whether you are a PhD student, who writes their final paper, a journalist working for a local newspaper, a screenwriter or a serios amazon reviewer – “Research Engine” (if deployed 😊) will definitely try to make the process of working on large texts easier for you. 

### Here is a brief review of all R.E. key features:

### • Quick References
Without even signing up for R.E. you are able to gain access to what it does best: namely helping you to cite properly given text-source. Currently R.E. can work with four kinds of text-based sources: books, chapters in edited books, articles and webpages. You just need to choose between whose 4 types and fill in the form. The resulted reference will be always given in two variations: APA (“American Psychological Association”) and MLA (Modern Language Association).

### • Sources
If you want to save a source and its reference for later use: no problem! Maybe you’d want to also add a link to this source or even upload a file containing this source – this would work smoothly! Delete or edit source later – yes of course!

### • Workspaces
When signed up, users will be invited to create their workspaces. The workspace is a main area where they will gather all their studies. It combines everything one needs to succeed at whiting any text: people, papers, sources and a bunch of features around. The workspace could be a place, where multiple members collaborate on writing different papers, or could tur into a fortress of solitude. But remember: you will be able to invite or share your workspace at any given time. And one more feature the developer is especially proud of: at actions area of your workspace, under a regular looking anchor tag, lies a possibility of downloading a zip-archive of your space with all files, papers, sources and references uploaded previously.

### • Papers
The paper you’re working on is of course the most important part of a workspace. On your paper’s page you will experience following: uploading and saving versions of your paper (pdf or docx), the quantity of pages, words and characters of your last uploaded file, choosing sources from your workspace in order to automatically get a bibliography for your page. Lastly, you will definitely find convenient, that R.E. can automatically add an automatically created bibliography to your last file.

## Technical Information

R.E. is built with Django on the back- and JavaScript, HTML and CSS on the frontend.

### Distinctiveness and Complexity

R.E. massively distinguishes from all other CS50W projects: neither social network, nor e-commerce site, it somehow keeps CS50W spirit: it’s simply and beautiful. The complexity of the project is really not so complicated to describe: R.E. on the backend part contains six (6!) Django apps (“bookshelf”, “file_handling”, “paper_work”, “work_space” and “user_management) and two python helper modules (“utils”, “citation”), which files are used across all apps. R.E has fifteen (15!) models altogether.

### R.E Applications

#### • user_management

This app does what it’s called: manages everything related to User model: registration, logging in, logging out, account settings (editing personal info), password changing, forgetting and resetting. 
Last feature works as it should be working: R.E. sends user email with a link and instructions how to reset an account password (see PasswordResetCode model).
helpers.py contains secondary functions for main view.py file.

####  • work_space

The app contains one of the main models of the project (WorkSpace) and two other models (Invitation and ShareSourcesCode) allowing to invite to or share a workspace. 

Secondary files: helpers.py, source_creation.py and source_sharing.py help preventing views.py from having different layers of abstraction in one place.

friendly_dir.py allows to create a temporary directory with all workspace related data, create a zip-file from it, download it and then deletes all that in less than a second.

#### • paper_work

The app manages two important modals: Paper and Bibliography (connected via OnetoOne model field).
Separate bibliography.py file makes possible to create, get, clear or update bibliography objects.

Besides that, app concentrates on Paper class. It allows to create, rename and archive it, transfer it to another workspace, clear files history, change its citation style (APA/MLA) or much more.

#### • bookshelf

“bookshelf” definitely has the most complex model structure. It uses [multi-table inheritance] (https://docs.djangoproject.com/en/5.0/topics/db/models/#model-inheritance) in order to store different types of sources:
class Source is a parent base class that has four child classes (Book, Article, Chapter, Webpage). Using _cast_ method one can access child class of any source-object.
Besides that, there is a Reference model with one-to-one relation to every source object that stores both APA and MLA endnotes.
source_alteration.py, source_citation.py, source_copying.py and soure_creation.py helping views.py to cope with all data.

#### • file_handling

Since uploading different files is a key feature of R.E., there is a separate “file_handling” app for this purpose. It deals with both .pdf and .docx files, storing and analyzing them (counting words, pages, characters etc.) 

#### • website
This app contains neither models nor forms. Its main purpose in life – to render!


### R.E. Modules

There are also two extra python modules created for R.E., so any app can access them.

#### • utils

Cleans data submitted via different Django forms (data_cleaning.py), provides the functionality of Django messages (messages.py) and keep the whole project secure (verification.py, decorators.py) checking if user has right to access given data.

#### • citation
Creates APA and MLA references. It’s built as a separate module, because this functionality use both bookshelf and website app (“quick reference” page).

### Frontend

On frontend side R.E. is made of Django Template Language (ten html files extend layout.html), CSS and JavaScript.
website.js – is a main js file with cross-page functions. Other js files improve user experience on every single R.E. page.


# Thank you CS50 ❤️❤️❤️
