#include "requests.hpp"
#include "db_usage.hpp"
#include <fstream>

int main(int argc, char* argv[])
{
    std::string PathToDb = "././database/schedule.db";
    std::ifstream ExistsDb(PathToDb);
    if (!ExistsDb.good()){
        database::open_db();
    }

    if (argc == 2 && std::string(argv[1]) == "clear") {
        database::clear_db();
        return 0;
    } else if (argc != 4) {
        std::cerr << "Wrong parameters" << std::endl;
        return -1;
    }

    const char* dep_station = argv[1];
    const char* arr_station = argv[2];
    const char* date = argv[3];
    requests::getRequest(dep_station, arr_station, date);

    return 0;
}
