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


    def get_int(bytes, offset, length, little_endian=False, signed=False):
        byte_order = "little" if little_endian else "big"
        return int.from_bytes(ByteUtility.get_bytes(bytes, offset, length), byteorder=byte_order, signed=signed)


    def get_bytes(data, offset: int, length: int) -> bytes:
        return data[offset:offset+length]


    def get_bit(byte, i):
        return (byte >> i) & 1
    

    def xor_bytes(a: bytes, b: bytes) -> bytes:
        if len(a) != len(b):
            raise ValueError("Cannot XOR non-equal length bytes")
        result = bytearray(a)
        for i, byte in enumerate(b):
            result[i] ^= byte
        return bytes(result)

    def get_encoded_string(data, version, lang, null_terminator="␀"):
        result = ""
        if version in (1,2,3,4,5,6,7):
            for c in ByteUtility.get_bytes(data, 0x0, len(data)):
                char = ByteUtility.get_encoded_character(c, version, lang)
                if (char != null_terminator):
                    result += char
                else:
                    break
        elif version in (8,9,10):
            for i, c in enumerate(ByteUtility.get_bytes(data, 0x0, len(data))):
                if i % 2 == 0:
                    char_bytes = ByteUtility.get_int(data, 0x0+i, 2, True)
                    char = ByteUtility.get_encoded_character(char_bytes, version, lang)
                    if (char != null_terminator):
                        result += char
                    else:
                        break
                else:
                    pass
        else:
            pass
        return result
    

    def get_encoded_character(character: int, generation: int, lang="en"):
        match generation:
            case 1 | 2:
                match lang:
                    case "en":
                        return CharacterEncoding.en_us_gen1.get(character, "")
                    case _:
                        pass
            case 3 | 4:
                match lang:
                    case "en":
                        return CharacterEncoding.en_us_gen2.get(character, "")
                    case _:
                            pass
            case 5 | 6 | 7:
                match lang:
                    case "en":
                        return CharacterEncoding.en_us_gen3.get(character, "")
                    case _:
                            pass
            case 8 | 9 | 10:
                match lang:
                    case "en":
                        return CharacterEncoding.western_gen4.get(character, "")
                    case _:
                        pass
        return "?"