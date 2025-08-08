#include <sqlite3.h>
#include <iostream>
#include "db_usage.hpp"

// Opens the database and creates the schedule table if it does not exist
void database::open_db(){ 
    sqlite3* db;
    int exit = sqlite3_open("././database/schedule.db", &db);

    if (exit) {
        std::cerr << "Can't open db: " << sqlite3_errmsg(db) << std::endl;
        return;
    } else {
        std::cout << "Db was opened succesfully" << std::endl;
    }

    // SQL statement to create the schedule table if it doesn't exist
    std::string sql_req = "CREATE TABLE IF NOT EXISTS schedule("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "date TEXT NOT NULL, "
                            "timezone TEXT NOT NULL, "
                            "departure_time TEXT NOT NULL,"
                            "departure_station TEXT NOT NULL, "
                            "arrival_time TEXT NOT NULL, "
                            "arrival_station TEXT NOT NULL, "
                            "type TEXT NOT NULL, "
                            "price TEXT NOT NULL);";
    char* errmsg = nullptr;
    exit = sqlite3_exec(db, sql_req.c_str(), 0, 0, &errmsg);

    if (exit != SQLITE_OK) {
        std::cerr << "table creating error: " << errmsg << std::endl;
        sqlite3_free(errmsg);
    } else {
        std::cout << "Table created succesfully" << std::endl;
    }

    sqlite3_close(db);
}

// Writes a schedule entry to the database
void database::write2db(std::string date, std::string timezone, std::string dep_time, std::string dep_station, std::string arr_time, std::string arr_station, std::string type, std::string price) {
    sqlite3* db;
    sqlite3_stmt* stmt;
    char* errmsg = nullptr;

    // Open the database
    if (sqlite3_open("././database/schedule.db", &db) != SQLITE_OK) {
        std::cerr << "Can't open db: " << sqlite3_errmsg(db) << std::endl;
        return;
    }

    // SQL statement to insert a new schedule entry
    const char* sql_request = "INSERT INTO schedule (date, timezone, departure_time, departure_station, arrival_time, arrival_station, type, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?);";

    // Prepare the SQL statement
    if (sqlite3_prepare_v2(db, sql_request, -1, &stmt, nullptr) != SQLITE_OK) {
        std::cerr << "Prepare error: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return;
    }

    // Bind parameters to the SQL statement
    sqlite3_bind_text(stmt, 1, date.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, timezone.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, dep_time.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 4, dep_station.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 5, arr_time.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 6, arr_station.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 7, type.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 8, price.c_str(), -1, SQLITE_STATIC);

    // Execute the SQL statement
    if (sqlite3_step(stmt) != SQLITE_DONE) {
        std::cerr << "Request error: " << sqlite3_errmsg(db) << std::endl;
    }

    // Finalize and close the database
    sqlite3_finalize(stmt);
    sqlite3_close(db);
}

// Clears all entries from the schedule table
void database::clear_db() {
    sqlite3* db;
    char* errmsg = nullptr;

    // Open the database
    if (sqlite3_open("././database/schedule.db", &db) != SQLITE_OK) {
        std::cerr << "Can't open db: " << sqlite3_errmsg(db) << std::endl;
        return;
    }

    // SQL statement to delete all entries and reset the autoincrement counter
    const char* sqlDelReq = "DELETE FROM schedule;"
                            "DELETE FROM sqlite_sequence WHERE name = 'schedule'";

    // Execute the SQL statement
    if (sqlite3_exec(db, sqlDelReq, nullptr, nullptr, &errmsg) != SQLITE_OK) {
        std::cerr << "Table deleting error" << errmsg << std::endl;
        sqlite3_free(errmsg);
    } else {
        std::cout << "Table cleaned succesfully" << std::endl;
    }

    sqlite3_close(db);
}

// Checks if a table exists in the database
bool database::table_exists(const std::string& table_name) {
    sqlite3* db;
    char* errmsg = nullptr;

    // Open the database
    if (sqlite3_open("././database/schedule.db", &db) != SQLITE_OK) {
        std::cerr << "Can't open db: " << sqlite3_errmsg(db) << std::endl;
        return false;
    }

    // SQL statement to check for table existence
    const char* sql =
        "SELECT count(*) "
        "  FROM sqlite_master "
        " WHERE type = 'table' AND name = ?;";

    sqlite3_stmt* stmt = nullptr;
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr) != SQLITE_OK) {
        std::cerr << "Failed to prepare statement: " 
                  << sqlite3_errmsg(db) << "\n";
        return false;
    }

    // Bind the table name parameter
    sqlite3_bind_text(stmt, 1, table_name.c_str(), -1, SQLITE_STATIC);

    bool exists = false;
    // Execute the statement and check if the table exists
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        int count = sqlite3_column_int(stmt, 0);
        exists = (count > 0);
    } else {
        std::cerr << "Failed to execute statement: " 
                  << sqlite3_errmsg(db) << "\n";
    }

    sqlite3_finalize(stmt);
    return exists;
}
