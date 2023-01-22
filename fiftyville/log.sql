-- Keep a log of any SQL queries you execute as you solve the mystery.
.schema
.schema crime_scene_reports
select description from crime_scene_reports where month = 7 and day = 28 and street = 'Humphrey Street';
--10:15am bakery
.schema bakery_security_logs
 select * from bakery_security_logs where year = 2021 and month = 7 and day = 28 and hour = 10;
 select license_plate from bakery_security_logs where year = 2021 and month = 7 and day = 28 and hour = 10;
--| R3G7486       |
--| 13FNH73       |
--| 5P2BI95       |
--| 94KL13X       |
--| 6P58WS2       |
--| 4328GD8       |
--| G412CB7       |
--| L93JTIZ       |
--| 322W7JE       |
--| 0NTHK55       |
--| 1106N58       |
--| NRYN856       |
--| WD5M8I6       |
--| V47T75I       |

select * from interviews where year = 2021 and month = 7 and day = 28;
-- ATM on Leggett Street  -- on the phone for less than a minute
select * from atm_transactions where atm_location = 'Leggett Street' and year = 2021 and month = 7 and day = 28;
select account_number from atm_transactions where atm_location = 'Leggett Street' and year = 2021 and month = 7 and day = 28;
--| 28500762       |
--| 28296815       |
--| 76054385       |
--| 49610011       |
--| 16153065       |
--| 86363979       |
--| 25506511       |
--| 81061156       |
--| 26013199       |
select name, people.id from people join bank_accounts on bank_accounts.person_id = people.id join atm_transactions on atm_transactions.account_number = bank_accounts.account_number where atm_transactions.account_number = 81061156;
select * from people where license_plate = 'WD5M8I6';
-- 660982 | Thomas | (286) 555-0131 | 6034823042      | WD5M8I6  not them :/
-- 398010 | Sofia | (130) 555-0289 | 1695452385      | G412CB7 not them :/
-- 221103 | Vanessa | (725) 555-4692 | 2963008352      | 5P2BI95   not them :/
-- 560886 | Kelsey | (499) 555-9472 | 8294398571      | 0NTHK55  not them :/
-- 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X them :)
select * from passengers where passport_number = 5773159633;
--| 36        | 5773159633      | 4A
select * from flights join passengers on passengers.flight_id = flights.id where passengers.flight_id = 36;
-- destination_airport_id = 4
select * from airports join flights on flights.destination_airport_id = airports.id where flights.destination_airport_id = 4;
 -- city = New York City
select * from phone_calls where caller = '(367) 555-5533';
select name from people where phone_number = '(375) 555-8161'; -- duration 45 them :)
    -- Name Robin
