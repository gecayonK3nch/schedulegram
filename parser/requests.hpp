#pragma once
#include <iostream>

// Namespace for handling HTTP requests to the schedule API
namespace requests {
    // Sends a request to the schedule API and writes results to the database
    // Returns 0 on success, -1 on error
    int getRequest(std::string from, std::string to, std::string date);
}

// Namespace for parsing and processing time-related strings
namespace parsing {
    // Extracts the time (HH:MM) from an ISO 8601 datetime string
    std::string parseTime(std::string time);

    // Calculates the arrival time given a departure time and duration (in seconds)
    std::string calculateArrivalTime(std::string dep_time, int duration);

    // Extracts the timezone offset (+HH:MM) from an ISO 8601 datetime string
    std::string parseTimeZone(std::string time);
}