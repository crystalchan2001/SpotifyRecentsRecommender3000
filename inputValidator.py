class InputValidator:

    def get_int(self, to_check):
        try:
            int(to_check)
        except:
            self.get_int(input("Please enter numbers only!: "))
        else:
            return int(to_check)
            
    def get_int_list(self, to_check):
        try:
            [eval(i) for i in to_check.strip().split()]
        except:
            self.get_int_list(input("Please only enter numbers separated by a space: "))
        else:
            return list([eval(i) for i in to_check.strip().split()])
            
    def get_valid_int(self, to_check, lowBound, upBound):
        num = self.get_int(to_check)
        valid_range = num in range(lowBound, upBound+1)
        while not valid_range:
            num = self.get_int(input(f"Please choose from the valid range between {lowBound} and {upBound}: "))
            valid_range = num in range(lowBound, upBound+1)
        return num

    # def get_valid_int_list(self, list_to_check, lowBound, upBound, limit):
    #     if (len(list_to_check) < 1 or len(list_to_check) > limit):
    #         self.get_valid_int_list(input(f"Please enter up to {limit} numbers: "))
    #     all_nums = self.get_int_list(list_to_check)
 

    def get_playlist_preference(self, to_check):
        invalid = True
        while invalid:
            if to_check.lower() == "new":
                return True
            elif to_check.lower() == "existing":
                return False
            else:
                to_check = input("Please enter either 'new' or 'existing': ")
