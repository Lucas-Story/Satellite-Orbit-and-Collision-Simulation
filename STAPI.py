import requests


class SpaceTrackAPI():
    def __init__(self,  username, password, update_other_3LEs_path):
        self.login_credentials = {"identity": username, "password": password}
        self.base_URL = "https://www.space-track.org"
        self.login_path = "/ajaxauth/login"
        self.update_other_3LEs_path = update_other_3LEs_path

    def update3LEs(self, other_file_path, my_file_path, NORAD_ID):

        # use a session to preserve cookies (need to preserve cookies so we are logged in when sending query)
        # use with block to ensure session always closes
        with requests.Session() as session:

            # log into space-track.org
            response = session.post(self.base_URL+self.login_path, data=self.login_credentials)
            # check that website recieved the log in attempt
            if response.status_code != 200:
                print(f"Error with login process. Status code: {response.status_code}")

            # query for all LEO sats
            response = session.get(self.base_URL+self.update_other_3LEs_path, stream=True)
            # stream=True: Ensures the response content is not loaded into memory all at once, which is useful for large files.
            # Check if the request was successful
            if response.status_code == 200:
                # Open a file in binary write mode
                with open(other_file_path, "wb") as file:
                    # Write the content of the response to the file in chunks
                    # iter_content(chunk_size=8192): Reads the response in manageable chunks to avoid memory issues.
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print("File for \"other satellites\" saved successfully!")
            else:
                print(f"Failed to fetch the file for \"other satellites\". Status code: {response.status_code}")
                session.close()
                return False

            # query for target sat
            response = session.get(self.base_URL+"/basicspacedata/query/class/gp/NORAD_CAT_ID/"+NORAD_ID+"/format/3LE", stream=True)
            # stream=True: Ensures the response content is not loaded into memory all at once, which is useful for large files.
            # Check if the request was successful
            if response.status_code == 200:
                # Open a file in binary write mode
                with open(my_file_path, "wb") as file:
                    # Write the content of the response to the file in chunks
                    # iter_content(chunk_size=8192): Reads the response in manageable chunks to avoid memory issues.
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print("File for \"my satellite\" saved successfully!")
                session.close()
                return True
            else:
                print(f"Failed to fetch the file for \"my satellite\". Status code: {response.status_code}")
                session.close()
                return False




if __name__ == "__main__":
    pass
