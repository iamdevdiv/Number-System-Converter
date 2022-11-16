class NumberSystemConverter():
    def __init__(self) -> None:
        self.digits = {  # base: digits
            2: ["0", "1", "."],
            8: ["0", "1", "2", "3", "4", "5", "6", "7", "."],
            10: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."],
            16: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "."]
        }
        self.hex_to_dec = {
            "A": 10,
            "B": 11,
            "C": 12,
            "D": 13,
            "E": 14,
            "F": 15,
        }
        self.dec_to_hex = {
            10: "A",
            11: "B",
            12: "C",
            13: "D",
            14: "E",
            15: "F"
        }
        self.base_text = {
            2: "binary",
            8: "octal",
            10: "decimal",
            16: "hexadecimal"
        }
        self.binary_to_oct_or_hex = {
            0: 0,
            1: 1,
            10: 2,
            11: 3,
            100: 4,
            101: 5,
            110: 6,
            111: 7,
            1000: 8,
            1001: 9,
            1010: "A",
            1011: "B",
            1100: "C",
            1101: "D",
            1110: "E",
            1111: "F"
        }

    def is_valid(self, num: str, num_base: int, conversion_base: int) -> bool:
        if type(num_base) != int:
            raise TypeError("Hi", f"integer argument expected in num_base, got {type(num_base).__name__}")
        elif type(conversion_base) != int:
            raise TypeError(f"integer argument expected in conversion_base, got {type(conversion_base).__name__}")
        elif type(num) != str:
            raise TypeError(f"string argument expected in num, got {type(num).__name__}")

        if num_base not in self.base_text.keys():
            raise ValueError(f"{num_base} is an invalid base.")
        elif conversion_base not in self.base_text.keys():
            raise ValueError(f"{conversion_base} is an invalid base.")

        num = num.upper()
        for digit in num:
            if digit not in self.digits[num_base]:
                raise ValueError(f"{num} is an invalid {self.base_text[num_base]} number.")
        
        if num.count(".") in [0, 1]:
            return True
        else:
            raise ValueError(f"{num} is an invalid {self.base_text[num_base]} number.")
    
    def get_superscript(self, num: str) -> str:
        normal = "0123456789-"
        super_s = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"
        table = num.maketrans(normal, super_s)
        return num.translate(table)
    
    def get_subscript(self, num: str) -> str:
        normal = "0123456789"
        sub_s = "₀₁₂₃₄₅₆₇₈₉"
        table = num.maketrans(normal, sub_s)
        return num.translate(table)
    
    # Converts binary/octal/hexadecimal numer to decimal number
    def to_decimal(self, num: str, num_base: int) -> None:
        integer_part, fraction_part = num.split(".")[0], ""
        if "." in num:
            fraction_part = num.split(".")[1]

        expansion, exp_to_print, solved_expansion = "", "", ""

        # Expand integer part
        for i, digit in enumerate(integer_part):
            if digit.isalpha():
                digit = self.hex_to_dec[digit]

            expansion += f"{digit}*{num_base}**{len(integer_part) - (i + 1)}"
            exp_to_print += f"{digit}*{num_base}{self.get_superscript(str(len(integer_part) - (i + 1)))}"
            if i != len(integer_part) - 1:
                expansion += " + "
                exp_to_print += " + "

        # Expand fraction part
        if len(fraction_part) > 0:
            expansion += " + "
            exp_to_print += " + "

            for i, digit in enumerate(fraction_part):
                if digit.isalpha():
                    digit = self.hex_to_dec[digit]

                expansion += f"{digit}*{num_base}**{- (i + 1)}"
                exp_to_print += f"{digit}*{num_base}{self.get_superscript(str(- (i + 1)))}"
                if i != len(fraction_part) - 1:
                    expansion += " + "
                    exp_to_print += " + "

        # Solve the expansion
        for i, expression in enumerate(expansion.split(" + ")):
            evaluation = eval(expression)
            if type(evaluation) == float and evaluation == 0:
                solved_expansion += str(int(eval(expression)))
            else:
                solved_expansion += str(eval(expression))

            if i != len(num.replace(".", "")) - 1:
                solved_expansion += " + "
        
        # Display the solution
        print(f"Solution for ({num}){self.get_subscript(str(num_base))} = (?){self.get_subscript('10')}:\n")
        print(exp_to_print)
        print(f"= {solved_expansion}")
        print(f"= ({eval(solved_expansion)}){self.get_subscript('10')}")
    
    # Converts decimal number to binary/octal/hexadecimal number
    def from_decimal(self, num: str, conversion_base: int) -> None:
        print(f"Solution for ({num}){self.get_subscript('10')} = (?){self.get_subscript(str(conversion_base))}:")

        integer_part, fraction_part = num.split(".")[0], ""
        if "." in num:
            fraction_part = float(f".{num.split('.')[1]}")
        
        new_int_part, new_frac_part = "", ""
        dividend = int(integer_part)
        width = None

        # Solve integer part
        if (dividend >= conversion_base and conversion_base in [2, 8]) or (dividend >= 16 and conversion_base == 16): 
            print(f"\n{conversion_base} | {integer_part}")
        while (dividend >= conversion_base and conversion_base in [2, 8]) or (dividend >= 16 and conversion_base == 16):
            print(("-" * len(integer_part)) + "-" * len(str(conversion_base)) + "-" * 4)

            remainder = str(dividend % conversion_base)
            if int(remainder) > 9:
                remainder = self.dec_to_hex[int(remainder)]
            new_int_part += remainder

            expression = f"{conversion_base} | {dividend // conversion_base}"
            if width is None:
                width = len(expression) + 4
            dividend = dividend // conversion_base
            if dividend < conversion_base:
                expression = expression.replace(str(conversion_base), " " * len(str(conversion_base)))

            print(expression.ljust(width, " "), f"{new_int_part[len(new_int_part) - 1]}")
        if dividend > 9:
            dividend = self.dec_to_hex[dividend]

        # Solve fraction part
        if len(str(fraction_part)) > 0:
            if len(new_int_part) > 0:
                print("")
            times_done = 0
            previous_fracs = []
            round_to = f"%.{len(num.split('.')[1])}f"
            while str(fraction_part).split(".")[1] != "0":
                fraction_part = float(f".{str(fraction_part).split('.')[1]}")
                if fraction_part in previous_fracs:
                    break
                previous_fracs.append(fraction_part)
                expression = f"{round_to % fraction_part} * {conversion_base} = {round_to % (fraction_part * conversion_base)}"

                fraction_part = fraction_part * conversion_base
                int_part = str(fraction_part).split(".")[0]
                if int_part not in previous_fracs:
                    print(expression, " " * (4 - len(int_part)), int_part)
                else:
                    break
                
                if int(int_part) > 9:
                    int_part = self.dec_to_hex[int(int_part)]
                new_frac_part += int_part

                times_done += 1
                if times_done == 8:
                    break
        
        # Display the answer
        answer = f"{dividend}{new_int_part[::-1]}"
        if len(new_frac_part) > 0:
            answer += f".{new_frac_part}"
        print(f"\n({num}){self.get_subscript('10')} = ({answer.lstrip('0')}){self.get_subscript(str(conversion_base))}")
    
    # Returns binary number converted from octal number (group_len=3) or hexadecimal number (group_len=4)
    def get_binary(self, num: str, group_len: int) -> str:
        binary = ""
        for digit in num:
            if digit == ".":
                binary += "."
            else:
                if digit.isalpha():
                    digit = self.hex_to_dec[digit]
                digit_in_binary = bin(int(digit)).replace("0b", "").rjust(group_len, "0")
                print(f"{digit} -> {digit_in_binary}")
                binary += digit_in_binary
        if "." in binary:
            binary = binary.rstrip("0")
        binary = binary.lstrip("0")
        return binary

    # Converts octal number to binary number using get_binary method
    def octal_to_binary(self, num: str, print_first_line=True) -> None:
        if print_first_line:
            print(f"Solution for ({num}){self.get_subscript('8')} = (?){self.get_subscript('2')}:\n")
        binary = self.get_binary(num, 3)
        print(f"\n({num}){self.get_subscript('8')} = ({binary}){self.get_subscript('2')}")
        return binary
    
    # Converts hexadecimal number to binary number using get_binary method
    def hexa_to_binary(self, num: str, print_first_line=True) -> None:
        if print_first_line:
            print(f"Solution for ({num}){self.get_subscript('16')} = (?){self.get_subscript('2')}:\n")
        binary = self.get_binary(num, 4)
        print(f"\n({num}){self.get_subscript('16')} = ({binary}){self.get_subscript('2')}")
        return binary
    
    # Returns octal number (group_len=3) or hexadecimal number (group_len=4) converted from binary number
    def from_binary(self, num: str, group_len: int) -> None:
        int_groups, frac_groups = [], []
        integer_part, fraction_part = num.split(".")[0], ""
        if "." in num:
            fraction_part = num.split(".")[1]
        
        # Solve integer part
        for i, char in enumerate(integer_part[::-1]):
            if i % group_len == 0:
                int_groups.append(f"{char}")
            else:
                int_groups[i // group_len] += char
        int_groups.reverse()
        int_groups = list(map(lambda x: x[::-1], int_groups))

        # Solve fraction part
        for i, char in enumerate(fraction_part):
            if i % group_len == 0:
                frac_groups.append(f"{char}")
            else:
                frac_groups[i // group_len] += char
        
        int_groups[0] = int_groups[0].rjust(group_len, "0")
        if len(frac_groups) > 0:
            frac_groups[-1] = frac_groups[-1].ljust(group_len, "0")
        
        # Return the resultant number
        all_groups = int_groups + ["."] + frac_groups if len(frac_groups) > 0 else int_groups
        result_num = ""
        for group in all_groups:
            if group == ".":
                result_num += "."
            else:
                result_num += str(self.binary_to_oct_or_hex[int(group)])
                print(f"{group} -> {self.binary_to_oct_or_hex[int(group)]}")
        if "." in result_num:
            result_num = result_num.rstrip("0")
        result_num = result_num.lstrip("0")
        return result_num

    # Converts binary number to octal number using from_binary method
    def binary_to_octal(self, num: str, print_first_line=True) -> None:
        if print_first_line:
            print(f"Solution for ({num}){self.get_subscript('2')} = (?){self.get_subscript('8')}:\n")
        octal_num = self.from_binary(num, 3)
        print(f"\n({num}){self.get_subscript('2')} = ({octal_num}){self.get_subscript('8')}")
    
    # Converts binary number to hexadecimal number using from_binary method
    def binary_to_hexa(self, num: str, print_first_line=True) -> None:
        if print_first_line:
            print(f"Solution for ({num}){self.get_subscript('2')} = (?){self.get_subscript('16')}:\n")
        hexa_num = self.from_binary(num, 4)
        print(f"\n({num}){self.get_subscript('2')} = ({hexa_num}){self.get_subscript('16')}")
    
    # Converts octal number to hexadecimal number using octal_to_binary and binary_to_hexa methods
    def octal_to_hexa(self, num: str) -> None:
        print(f"Solution for ({num}){self.get_subscript('8')} = (?){self.get_subscript('16')}:\n")
        binary_num = self.octal_to_binary(num, False)
        print("")
        self.binary_to_hexa(binary_num, False)
    
    # Converts hexadecimal number to octal number using hexa_to_binary and binary_to_octal methods
    def hexa_to_octal(self, num: str) -> None:
        print(f"Solution for ({num}){self.get_subscript('8')} = (?){self.get_subscript('16')}:\n")
        binary_num = self.hexa_to_binary(num, False)
        print("")
        self.binary_to_octal(binary_num, False)

    # Use this method to convert numbers from one system to another
    def convert(self, num: str, num_base: int, conversion_base: int) -> None:
        self.is_valid(num, num_base, conversion_base)
        num = num.upper()

        if num_base == conversion_base:
            lhs = rhs = f"({num}){self.get_subscript(str(num_base))}"
            print(f"{lhs} = {rhs}")
        elif conversion_base == 10:  # binary/octal/hexadecimal => decimal
            self.to_decimal(num, num_base)
        elif num_base == 10:  # decimal => binary/octal/hexadecimal
            self.from_decimal(num, conversion_base)
        elif num_base == 8 and conversion_base == 2:  # octal => binary
            self.octal_to_binary(num)
        elif num_base == 16 and conversion_base == 2:  # hexadecimal => binary
            self.hexa_to_binary(num)
        elif num_base == 2 and conversion_base == 8:  # binary => octal
            self.binary_to_octal(num)
        elif num_base == 2 and conversion_base == 16:  # binary => hexadecimal
            self.binary_to_hexa(num)
        elif num_base == 8 and conversion_base == 16:  # octal => hexadecimal
            self.octal_to_hexa(num)
        elif num_base == 16 and conversion_base == 8:  # hexadecimal => octal
            self.hexa_to_octal(num)


if __name__ == "__main__":
    converter = NumberSystemConverter()

    print("----- NUMBER SYSTEM CONVERTER -----")
    while True:
        num = input("\nEnter space-seperated values of:\n1. The number to be converted\n2. Its base\n3. The base to which you want it to convert\n(or q to exit)\n")
        if num.lower() == "q":
            break

        try:
            num, num_base, conversion_base = num.split()
            converter.convert(num, int(num_base), int(conversion_base))
        except (TypeError, ValueError):
            print("Invalid input! Please read the instructions carefully and provide input accordingly...")
