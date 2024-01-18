class InputValidator:

    def is_int(self, to_check):
        try:
            int(to_check)
        except:
            return False
        else:
            return True
            
    def is_int_list(self, to_check):
        try:
            [int(i) for i in to_check]
        except:
            return False
        else:
            return True
    
    def is_in_range(self, to_check, upBound):
        return (int(to_check) > 0 and int(to_check) <= upBound)
    
    def get_valid_int(self, to_check, upBound):
        invalid = True
        result = None

        while invalid:
            invalid_int = not self.is_int(to_check)
            if invalid_int:
                to_check = input("Please enter a number: ")
                continue
            invalid_range = not self.is_in_range(to_check, upBound)
            if invalid_range:
                to_check = input(f"Please enter a number between 1 and {upBound}: ")
                continue
            else: 
                result = int(to_check)
                invalid = False
        
        return result
    
    def get_valid_seeds(self, to_check, upBound):
        invalid = True
        indexes = []

        while invalid:
            indexes = to_check.strip().split()
            invalid_int_list = not self.is_int_list(indexes)
            if invalid_int_list:
                to_check = input("Please enter numbers separated by spaces: ")
                continue
            invalid_list_length = len(indexes) < 1 or len(indexes) > 5
            if invalid_list_length:
                to_check = input("Please enter up to 5 indexes: ")
                continue
            invalid_seed_values = not all(self.is_in_range(int(idx), upBound) for idx in indexes)
            if invalid_seed_values:
                to_check = input(f"Please enter indexes between 1 and {upBound}: ")
                continue  
            else:
                invalid = False     

        return indexes

    def get_playlist_preference(self, to_check):
        invalid = True
        while invalid:
            if to_check.lower() == "new":
                return True
            elif to_check.lower() == "existing":
                return False
            else:
                to_check = input("Please enter either 'new' or 'existing': ")
