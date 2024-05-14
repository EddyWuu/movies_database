import constants
import mysql.connector

# main loop for our main menu
def main():
    print("Welcome to ECE Movie Database!\n\n")
    command = ""

    # loop here that only exits when 'exit' is typed in
    while command != "exit":

        # instantiating our user (database) every time the loop resets
        user = mainUser()

        try:
            command = input("\nPlease enter your desired command. Type help for help and a list of commands.\n")

            if not isValid(command):
                print("Invalid input. Please try again.\n")
            else:
                if command == "help":
                    helpFunction()

                elif command == "search_m":
                    user.search_m_function()

                elif command == "add_m":
                    user.add_m_function()

                elif command == "create_r":
                    user.create_r_function()

                elif command == "modify_r":
                    user.modify_r_function()

                elif command == "view_r":
                    user.view_r_function()

                elif command == "delete_r":
                    user.delete_r_function()
   
        except KeyboardInterrupt:
            # should only exit when 'exit' is typed
            print("Ctrl-C detected. If you wish to exit, please type 'exit'\n\n")

    print("\nExiting client...")
    return 0



# DB instantiation -----------------------------------------------------------

# shouldn't have the passwords here, but for now we will keep them
class mainDB:
    host = "marmoset06.shoshin.uwaterloo.ca"
    port = ""
    user = "m29deng"
    password = "dbDztJEFER3!ovUiwa!3"
    database = "db356_team19"
    connection = None
    cursor = None

    def get_connector():
        mainDB.connection = mysql.connector.connect(
                host=mainDB.host,
                # port=mainDB.port,
                user=mainDB.user,
                password=mainDB.password,
                database=mainDB.database
                )
        return mainDB.connection
    
    def get_cursor():
        if mainDB.connection is None:
            mysql.connector()
        
        mainDB.cursor = mainDB.connection.cursor()
        return mainDB.cursor


# main user and its functions ------------------------------------------------------------

class mainUser():
    def __init__(self): # Init - we need the connector and cursor
        self.id = 0
        self.connector = mainDB.get_connector()
        self.cursor = mainDB.get_cursor()

    #-- the rest of the functionality

    def search_m_function(self):
       
        # the flow of this function is as follows:
            # 1. display each of the columns to the user and ask them for which ones they'd like to select
            # 2. Ask the user how many filters they would like to create. These are essentially 'where' clauses'.
            # 3. Take in these filters
            # 4. Potentially ask for a ORDERBY statement
            # 5. Build and run the query, and output it. 

        # it also has try catch blocks to catch any errors on input or SQL errors.

        try:
            self.cursor.execute(f"SELECT * FROM {constants.main_movie_table} LIMIT 1")
            table_types = self.cursor.fetchone() # have to fetch this to clear the cursor for the next execute
            num_fields = len(self.cursor.column_names)
            field_names = [i for i in self.cursor.column_names]

            print("\n\nFirst, you will select the columns to view. Then, you will select the columns to search on, and give a matching filter. Then, you will give a column to order by. If you have no specific preferences at each point, just press enter")
            print("\nThese are the common movie properties to view: ")
            print(" ".join(field_names))

            basic_properties = input("\nPlease enter the columns you wish to view, separated by spaces.\n")
            search_properties = []
            num_search = int(input("\nNow, please enter the number of filters you'd like to create. (ex. search by date and budget)\n"))


            for i in range(num_search):
                column = input(f"\nPlease enter the searched name of Column {i+1}\n")
                value = input(f"\nPlease enter the desired value of Column {i+1}\n")

                search_properties.append((column, value))

            order_by_columns = input("\nOptionally, enter ONE column you wish to ORDER BY.\n")
            # build up query

            base_query = f"SELECT {', '.join(basic_properties.split(' '))} FROM {constants.main_movie_table} "
            where_clause = ""
            order_clause = ""
            if len(search_properties):
                where_clause = f"WHERE {search_properties[0][0]} = '{search_properties[0][1]}' "

            if len(search_properties) > 1:
                for i in range(1, len(search_properties)):
                    where_clause += f"AND {search_properties[i][0]} = '{search_properties[i][1]}' "


            if order_by_columns:
                order_clause = f"ORDER BY {order_by_columns}"

            order_clause = order_clause + ";"
            entire_query = base_query + where_clause + order_clause
            # print(f"\nQUERY IS:\n{entire_query}\n")
            
            
            # execute query
            try:
                self.cursor.execute(entire_query)
                tuples = self.cursor.fetchall()

                print(self.cursor.column_names)

                if tuples:
                    for row in tuples:
                        print(row)

                    print("\n")
                else:
                    print("There are no movies that match your filter(s). Please try again.")

            except Exception as e:
                print("SQL Error occurred")
                print(e)
                print("\n")
                self.close_everything()
                return


        except Exception as e:
            print("An unexpected error occurred. Please try again.\n")
            print(e)
            self.close_everything()
            return
        


    def add_m_function(self):
        # This function can add movies to the main movie database given that the user has all the required information for it. 
        # If they don't, they will return to the main menu. This stops users from inputting incorrect or missing data.

        print("\nYou are about to add a movie to the database. Only continue if you are sure and have all the data required.\n")
        
        movieID = input("\nEnter the movie id of the movie you wish to review.\n")
        title = input("\nPlease enter your the title of the movie.\n")
        description = input("\nPlease enter a description of the movie.\n")
        mpaa = input("\nPlease enter the mpaa of the movie\n")
        releaseDate = input("\nPlease enter the release date\n")
        duration = input("\nPlease enter the duration of the movie\n")
        budget = input("\nPlease enter the budget of the movie\n")

        if movieID and title and description and mpaa and duration and budget:
            #they are all not empty

            try:
                self.cursor.execute(f"INSERT INTO {constants.main_movie_table}(movieID, title, movieDescription, mpaa, duration, releaseDate, budget) VALUES ('{movieID}', '{title}', \"{description}\",'{mpaa}', '{releaseDate}', '{duration}', {budget});")
                self.connector.commit()
                self.close_everything()
                print("Movie succesfully added")

            except Exception as e:
                print("SQL Error occurred")
                print(e)
                print("\n")
                self.close_everything()
                return

        else:
            print("Please fill in all the fields. Please try again")
            return
                
        return



    def search_p_function(self):
        
        # This function is almost the same as search_m. We search for a person based off different filers, build the query, and execute it.

        cast_or_crew = input("\nAre you searching for a cast member or a crew member? (Type 'cast' or 'crew')\n")

        if cast_or_crew != "crew" and cast_or_crew != "cast":
            print("\nPlease exit and try again.")
            return
        
        try:
           
            print("\n\nFirst, you will select the columns to view. Then, you will select the columns to search on, and give a matching filter. Then, you will give a column to order by. If you have no specific preferences at each point, just press enter")
            print("\nThese are the common movie properties to view: ")
            print("PersonID, MovieID, Role, BirthName, DOB")

            search_properties = []
            num_search = int(input("\nNow, please enter the number of filters you'd like to create. (ex. search by role or name)\n"))


            for i in range(num_search):
                column = input(f"\nPlease enter the searched name of Column {i+1}\n")
                value = input(f"\nPlease enter the desired value of Column {i+1}\n")

                search_properties.append([column, value]) # list of lists

            order_by_columns = input("\nOptionally, enter ONE column you wish to ORDER BY.\n")
            # build up query

            base_query = f"""SELECT 
p.personID as person_id
p.name AS person_name,
p.birthdate AS person_birthdate,
COALESCE(c.cast_role, 'N/A') AS cast_role,
COALESCE(cr.crew_role, 'N/A') AS crew_role,
COALESCE(c.movieID, cr.movieID) AS movie_id
FROM 
    {constants.main_person_table} p
JOIN 
    {constants.main_cast_table} c ON p.personID = c.personID
JOIN 
    {constants.main_crew_table} cr ON p.personID = cr.personID
            """

            where_clause = ""
            order_clause = ""

            # cast human readable names to proper sql columns in the join

            for search in search_properties:
                if search[0] == "PersonID":
                    search[0] = "p.personID"
                elif search[0] =="MovieID":
                    search[0] = "movie_id"
                elif search[0] == "Role":
                    if cast_or_crew == "cast":
                        search[0] = "c.cast_role"
                    else:
                        search[0] = "cr.crew_role"
                elif search[0] == "BirthName":
                    search[0] = "p.name"
                elif search[0] == "DOB":
                    search[0] = "p.birthdate"


                if order_by_columns == "PersonID":
                    order_by_columns = "p.personID"
                elif order_by_columns =="MovieID":
                    order_by_columns = "movie_id"
                elif order_by_columns == "Role":
                    if cast_or_crew == "cast":
                        order_by_columns = "c.cast_role"
                    else:
                        order_by_columns = "cr.crew_role"
                elif order_by_columns == "BirthName":
                    order_by_columns = "p.name"
                elif order_by_columns == "DOB":
                    order_by_columns = "p.birthdate"



            if len(search_properties):
                where_clause = f"WHERE {search_properties[0][0]} = '{search_properties[0][1]}' "

            if len(search_properties) > 1:
                for i in range(1, len(search_properties)):
                    where_clause += f"AND {search_properties[i][0]} = '{search_properties[i][1]}' "


            if order_by_columns:
                order_clause = f"ORDER BY {order_by_columns}"

            order_clause = order_clause + ";"
            entire_query = base_query + where_clause + order_clause
            print(f"\nQUERY IS:\n{entire_query}\n")
            
            
            # execute query
            try:
            # self.cursor = self.cursor(buffered=True)

                self.cursor.execute(entire_query)
                tuples = self.cursor.fetchall()
                # print(tuples)
                print(self.cursor.column_names)

                if tuples:
                    for row in tuples:
                        print(row)

                    print("\n")
                else:
                    print("There are no people that match your filter(s). Please try again.")

            except Exception as e:
                print("SQL Error occurred")
                print(e)
                print("\n")
                self.close_everything()
                return


        except Exception as e:
            print("An unexpected error occurred. Please try again.\n")
            print(e)
            self.close_everything()
            return
        return
    

    def create_r_function(self):
        
        # this function creates a review. The flow is as follows:
            # first, make sure the movieID is valid. 
            # then, we make sure a review does not exist already.
            # given these two, we take in the custom rating and custom description. We then use a INSERT to update this in the review table

        movieID = input("\nEnter the movie id of the movie you wish to review.\n")

        self.cursor.execute(f"SELECT TITLE FROM {constants.main_movie_table} WHERE movieID='{movieID}';")
        movie_title = self.cursor.fetchone()[0]

        if movie_title:
            # do something
            self.cursor.execute(f"SELECT * FROM {constants.main_review_table} WHERE movieID='{movieID}';")
            review_exists = self.cursor.fetchone()
            
            if not review_exists:
                # create a review
                rating = input("\nPlease enter your rating from 1-10 for the movie.\n")
                description = input("\nOptionally, enter a further detailed review.\n")
                
                self.cursor.execute(f"INSERT INTO {constants.main_review_table}(movieID, title, customRating, customReview) VALUES ('{movieID}', '{movie_title}', {rating},\"{description}\");")
                self.connector.commit()
                self.close_everything()

                print("\nReview succesfully added.")
            else:
                print("You already created a review for this movie. Please modify the review with the 'modify_r_function'")
                self.close_everything()

        else:
            print("That movie doesn't exist. Please try again.")
            self.close_everything()
   
        return
    


    def modify_r_function(self):
        # this function modifies a review. It works as follows:
            # Make sure the movieID is valid
            # make sure a review already exists. If not, return to the main menu.
            # given these two, we take in the custom rating and description, and use an UPDATE SET statement to update our entry

        movieID = input("\nEnter the movie id of the reviewed movie you wish to modify.\n")

        self.cursor.execute(f"SELECT * FROM {constants.main_movie_table} WHERE movieID='{movieID}';")
        movie = self.cursor.fetchone()
        if movie:
            # do something
            self.cursor.execute(f"SELECT * FROM {constants.main_review_table} WHERE movieID='{movieID}';")
            review_exists = self.cursor.fetchone()
            
            if review_exists:
                # modify the review
                rating = input("\nPlease enter your new rating from 1-10 for the movie.\n")
                description = input("\nOptionally, enter the new further detailed review.\n")
                
                self.cursor.execute(f"UPDATE {constants.main_review_table} SET customReview = \"{description}\", customRating = {rating} WHERE movieID = '{movieID}';")
                self.connector.commit()
                self.close_everything()

                print("\nReview succesfully modified.")

            else:
                print("There is no review associated with this movie. Please use 'create_r_function' to create a review")
                self.close_everything()


        else:
            print("That movie doesn't exist. Please try again.")
            self.close_everything()

        return
    


    def view_r_function(self):
        # this function simply views a review for a movie ID. It works as follows:
            # first, make sure the movieID exists. 
            # then, make sure a review exists.
            # given these two, print out the review and rating. 

        movieID = input("\nEnter the movie id of the movie you wish to view.\n")

        self.cursor.execute(f"SELECT * FROM {constants.main_movie_table} WHERE movieID='{movieID}';")
        movie = self.cursor.fetchone()
        if movie:
            # do something
            self.cursor.execute(f"SELECT * FROM {constants.main_review_table} WHERE movieID='{movieID}';")
            review_exists = self.cursor.fetchone()

            print(review_exists)
            
            if review_exists:
                # view the review
                print(f"\nThe title of the movie is: {review_exists[1]}")
                print(f"Your rating was: {review_exists[2]}")
                print(f"Your description was: {review_exists[3]}")
                self.close_everything()
                
            else:
                print("There is no review associated with this movie. Please use 'create_r_function' to create a review")
                self.close_everything()


        else:
            print("That movie doesn't exist. Please try again.")
            self.close_everything()

        return
    
    
    def delete_r_function(self):
        # this function deletes a review for a movie ID. It works as follows:
            # first, make sure the movieID exists. 
            # then, make sure a review exists.
            # then, use DELETE FROM to delete the entry from the review table

        movieID = input("\nEnter the movie id of the movie review you wish to delete.\n")

        self.cursor.execute(f"SELECT * FROM {constants.main_movie_table} WHERE movieID='{movieID}';")
        movie = self.cursor.fetchone()
        if movie:
            # do something
            self.cursor.execute(f"SELECT * FROM {constants.main_review_table} WHERE movieID='{movieID}';")
            review_exists = self.cursor.fetchone()
            
            if review_exists:
                # delete the review
                self.cursor.execute(f"DELETE FROM {constants.main_review_table} WHERE movieID = '{movieID}';")
                self.connector.commit()
                print("Review deleted succesfully.\n")
                self.close_everything()
                
            else:
                print("There is no review associated with this movie. Please use 'create_r_function' to create a review.\n")
                self.close_everything()

        else:
            print("That movie doesn't exist. Please try again.\n")
            self.close_everything()
        return
    

    # this function helps to reset the cursor and connector. It makes it so the database cursor and connector are cleared in the event of an error or successful final query
    def close_everything(self):
        self.cursor.reset()
        self.cursor.close()
        self.connector.close()



# helper functions--------------------------------------------------------------------

def helpFunction():
    help_string = """
These are the current functions of this client:

"search_m": search for a specific movie based on certain filters
"add_m": add a movie given all the required information
"search_p": search for a specific person based on certain filters
"create_r": create a movie review
"modify_r": modify a movie review
"view_r": view the reviews for a movie
"delete_r": delete an exisitng movie review
"exit": exit out of the client
    """
    print(help_string)


def isValid(command:str) -> bool:
    command = command.lower().strip()

    if command in constants.FUNCTIONS:
        return True
    else:
        return False


# entry into program, call main method
if __name__ == "__main__":
    main()