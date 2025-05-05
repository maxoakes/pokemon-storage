from CharacterEncoding import CharacterEncoding


class ByteUtility:
    
    def get_string(bytes: str, generation: int, lang: str):
        output = ""
        for c in bytes:
            char = ByteUtility.get_encoded_character(c, generation, lang)
            if (char != "[end]"):
                output += char
            else:
                break
        return output


    def get_int(bytes, offset, length, little_endian=False):
        if little_endian:
            return int.from_bytes(ByteUtility.get_bytes(bytes, offset, length)[::-1])
        else:
            return int.from_bytes(ByteUtility.get_bytes(bytes, offset, length))


    def get_bytes(data, offset: int, length: int) -> bytes:
        return data[offset:offset+length]


    def get_bit(byte, i):
        return (byte >> i) & 1

    def get_encoded_string(data, version, lang, null_terminator="[end]"):
        result = ""
        for c in ByteUtility.get_bytes(data, 0x0, len(data)):
            char = ByteUtility.get_encoded_character(c, version, lang)
            if (char != null_terminator):
                result += char
            else:
                break
        return result
    

    def get_encoded_character(character, generation: int, lang="en"):  
        match generation:
            case 1 | 2:
                match lang:
                    case "en":
                        return CharacterEncoding.en_us_gen1.get(character, "?")
                    case _:
                        pass
            case 3 | 4:
                match lang:
                    case "en":
                        return CharacterEncoding.en_us_gen2.get(character, "?")
                    case _:
                            pass
            case 5 | 6 | 7:
                match lang:
                    case "en":
                        return CharacterEncoding.en_us_gen3.get(character, "?")
                    case _:
                            pass
        return "?"