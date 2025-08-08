#include "requests.hpp"
#include "db_usage.hpp"
#include <cpr/cpr.h>
#include <nlohmann/json.hpp>

// Sends a request to the schedule API and writes results to the database
int requests::getRequest(std::string from, std::string to, std::string date) {

    // Path to the JSON file containing API URL and key
    std::string PathToFile = "././parser/params.json";
    std::ifstream inputFile(PathToFile);

    // Check if the file can be opened
    if (!inputFile.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return -1;
    }

    // Parse the JSON file for API parameters
    nlohmann::json j;
    inputFile >> j;
    inputFile.close();

    std::string url = j["URL"];
    std::string api_key = j["API_KEY"];

    j.clear();

    // Set transport type to suburban trains
    std::string transport_type = "suburban";

    // Send GET request to the API
    auto request = cpr::Get(cpr::Url{ url },
                    cpr::Parameters{{"apikey", api_key},
                                    {"from", from},
                                    {"to", to},
                                    {"date", date},
                                    {"transport_types", transport_type}});
    // Handle request errors
    if (request.error) {
        std::cerr << "Request failed: " << request.error.message << std::endl;
    }

    // Parse the JSON response
    j = nlohmann::json::parse(request.text);

    // Iterate over each segment (train ride) in the response
    for (nlohmann::json el : j["segments"]) {
        try {
            // Extract departure time and duration
            std::string departure_time = el["departure"];
            int duration = el["duration"];
            std::string price = "Ушел"; // Default price if not available

            // Try to extract ticket price if available
            if (el.contains("tickets_info")) {
                if (!el["tickets_info"].is_null()){
                    nlohmann::json tickets_info = el["tickets_info"];
                    nlohmann::json ticket = tickets_info["places"][0];
                    if (!ticket.is_null()){
                        nlohmann::json prices = ticket["price"];
                        price = std::to_string(int(prices["whole"]));
                    } else {
                        price = "Неизвестно";
                    }
                }
            }

            // Extract transport subtype (e.g., train type)
            nlohmann::json transport_subtype = el["thread"];
            nlohmann::json subtype = transport_subtype["transport_subtype"];
            std::string type = subtype["title"];

            // Write the parsed data to the database
            database::write2db(
                date,
                parsing::parseTimeZone(departure_time),
                parsing::parseTime(departure_time),
                from,
                parsing::calculateArrivalTime(parsing::parseTime(departure_time), duration),
                to,
                type,
                price
            );
        } catch (...) {
            // Handle any parsing or data errors
            std::cerr << "An error occured" << std::endl;
            std::cout << el << std::endl;
        }
    }

    std::cout << "Data succesfully added!" << std::endl;

    return 0;
}

// Extracts the time (HH:MM) from an ISO 8601 datetime string
std::string parsing::parseTime(std::string time) {
    return time.substr(time.find('T') + 1, 5);
}

// Extracts the timezone offset (+HH:MM) from an ISO 8601 datetime string
std::string parsing::parseTimeZone(std::string time) {
    return time.substr(time.find('+'), 6);
}

// Calculates the arrival time given a departure time and duration (in seconds)
std::string parsing::calculateArrivalTime(std::string dep_time, int duration) {
    // Parse hours and minutes from departure time
    int hours = std::stoi(dep_time.substr(0, 2));
    int minutes = std::stoi(dep_time.substr(3, 2));

    // Convert departure time to seconds and add duration
    int summary_time = hours * 3600 + minutes * 60 + duration;

    // Calculate resulting hours and minutes, wrap around 24h
    int res_hours = (summary_time / 3600) % 24;
    int res_minutes = (summary_time / 60) % 60;

    // Format arrival time as HH:MM
    std::ostringstream ArrivalTime;
    ArrivalTime << std::setw(2) << std::setfill('0') << res_hours << ":"
                << std::setw(2) << std::setfill('0') << res_minutes;
    return ArrivalTime.str();
}
