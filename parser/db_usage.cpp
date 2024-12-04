#include <sqlite3.h>
#include <iostream>
#include "db_usage.hpp"

void database::open_db(){ 
    sqlite3* db;
    int exit = sqlite3_open("C:/Users/gecay/OneDrive/Desktop/Projects/Bots/schedulegram/database/schedule.db", &db);

    if (exit) {
        std::cerr << "Can't open db: " << sqlite3_errmsg(db) << std::endl;
        return;
    } else {
        std::cout << "Db was opened succesfully" << std::endl;
    }

    std::string sql_req = "CREATE TABLE IF NOT EXISTS schedule("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "date TEXT NOT NULL, "
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

void database::write2db(std::string date, std::string dep_time, std::string dep_station, std::string arr_time, std::string arr_station, std::string type, std::string price) {
    sqlite3* db;
    sqlite3_stmt* stmt;
    char* errmsg = nullptr;

    if (sqlite3_open("C:/Users/gecay/OneDrive/Desktop/Projects/Bots/schedulegram/database/schedule.db", &db) != SQLITE_OK) {
        std::cerr << "Can't open db: " << sqlite3_errmsg(db) << std::endl;
        return;
    }

    const char* sql_request = "INSERT INTO schedule (date, departure_time, departure_station, arrival_time, arrival_station, type, price) VALUES (?, ?, ?, ?, ?, ?, ?);";

    if (sqlite3_prepare_v2(db, sql_request, -1, &stmt, nullptr) != SQLITE_OK) {
        std::cerr << "Prepare error: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return;
    }

    sqlite3_bind_text(stmt, 1, date.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, dep_time.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, dep_station.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 4, arr_time.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 5, arr_station.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 6, type.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 7, price.c_str(), -1, SQLITE_STATIC);

    if (sqlite3_step(stmt) != SQLITE_DONE) {
        std::cerr << "Request error: " << sqlite3_errmsg(db) << std::endl;
    } else {
        std::cout << "Data succesfully added!" << std::endl;
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);
}

void database::clear_db() {
    sqlite3* db;
    char* errmsg = nullptr;

    if (sqlite3_open("C:/Users/gecay/OneDrive/Desktop/Projects/Bots/schedulegram/database/schedule.db", &db) != SQLITE_OK) {
        std::cerr << "Can't open db: " << sqlite3_errmsg(db) << std::endl;
        return;
    }

    const char* sqlDelReq = "DELETE FROM schedule;";

    if (sqlite3_exec(db, sqlDelReq, nullptr, nullptr, &errmsg) != SQLITE_OK) {
        std::cerr << "Table deleting error" << errmsg << std::endl;
        sqlite3_free(errmsg);
    } else {
        std::cout << "Table cleaned succesfully" << std::endl;
    }

    sqlite3_close(db);
}
