#include "requests.hpp"
#include "db_usage.hpp"
#include <fstream>

// Entry point of the parser application
int main(int argc, char* argv[])
{
    // Path to the SQLite database file
    std::string PathToDb = "././database/schedule.db";
    std::ifstream ExistsDb(PathToDb);

    // Check if the database exists and the table "schedule" exists, otherwise create them
    if (!ExistsDb.good() || !database::table_exists("schedule")) {
        database::open_db();
    }

    // If the user wants to clear the database, handle the "clear" command
    if (argc == 2 && std::string(argv[1]) == "clear") {
        database::clear_db();
        return 0;
    } 
    // If the arguments are not as expected, print an error
    else if (argc != 4) {
        std::cerr << "Wrong parameters" << std::endl;
        return -1;
    }

    // Parse command line arguments for departure station, arrival station, and date
    const char* dep_station = argv[1];
    const char* arr_station = argv[2];
    const char* date = argv[3];

    // Fetch schedule data and write it to the database
    requests::getRequest(dep_station, arr_station, date);

    return 0;
}
