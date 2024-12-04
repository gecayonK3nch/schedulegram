#pragma once
#include <iostream>

namespace database {
    void write2db(std::string date,
                std::string dep_time,
                std::string dep_station,
                std::string arr_time,
                std::string arr_station,
                std::string type,
                std::string price);
    void clear_db();
    void open_db();
}
