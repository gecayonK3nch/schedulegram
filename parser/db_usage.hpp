#pragma once
#include <iostream>

// Namespace for database operations
namespace database {
    // Writes a schedule entry to the database
    void write2db(std::string date,
                std::string timezone,
                std::string dep_time,
                std::string dep_station,
                std::string arr_time,
                std::string arr_station,
                std::string type,
                std::string price);

    // Clears all entries from the schedule table
    void clear_db();

    // Opens the database and creates the schedule table if it does not exist
    void open_db();

    // Checks if a table exists in the database
    bool table_exists(const std::string& table_name);
}
