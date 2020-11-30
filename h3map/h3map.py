import gzip
import struct
import sys



def get_format_string(repetitions, character):
    return str(repetitions) + character


def parse_header(buffer):
    version = struct.unpack('I', buffer[:4])
    any_players = struct.unpack('?', buffer[4:5])
    height = struct.unpack('I', buffer[5:9])
    two_level = struct.unpack('?', buffer[6:7])
    size_name = struct.unpack('I', buffer[10:14])[0]

    end_name = 14 + size_name
    name = struct.unpack(get_format_string(size_name, "s"), buffer[14:end_name])

    size_desc = struct.unpack('I', buffer[end_name:end_name + 4])[0]
    desc = struct.unpack(get_format_string(size_desc, "s"), buffer[end_name + 4:end_name + 4 + size_desc])

    end_desc = end_name + 4 + size_desc
    diff = struct.unpack('B', buffer[end_desc:end_desc+1])

    max_level = struct.unpack('B', buffer[end_desc+1:end_desc+2])

    print("Version: ", version)
    print("any players: ", any_players)
    print("height: ", height)
    print("two level: ", two_level)
    print("size of name: ", size_name)
    print("name: ", name)
    print("size of desc: ", size_desc)
    print("description: ", desc)
    print("difficulty: ", diff)
    print("max hero level: ", max_level)


def parse_player_info(content):
    pass



def main(map_contents):
    parse_header(map_contents)
    #parse_player_info(remaining)
    #parse_victory_loss_conditions()
    #parseTeamInfo()
    #parseAllowedHeroes()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("No map provided")

    map_file = sys.argv[1]
    map_contents = gzip.open(map_file, 'rb').read()
    main(map_contents)
