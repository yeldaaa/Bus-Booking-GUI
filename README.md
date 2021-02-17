# Bus-Booking-GUI
Submission for BC0401 Project 

This GUI was developed by [Adley Goh](https://www.linkedin.com/in/adley-goh-2a1452193/), [Jackson Tang](https://www.linkedin.com/in/jackson-tang-b91260196/), [Ethan Looi](https://www.linkedin.com/in/ethanlooi/), [Lee Ting Wen](https://www.linkedin.com/in/leetingwen/), and, [Chin Min Ray](https://www.linkedin.com/in/minray/).

Our team came up with this idea to develop an application for students in NTU to be able to book and secure their [shuttle bus](https://www.ntu.edu.sg/has/Transportation/Pages/GettingToNTU.aspx) seats the day before and not be left stranded. 

## Current Situation
Students that want to take the shuttle bus to school will have to queue up ahead of time in order to get a seat on the bus and once the bus reaches its maximum capacity, the remaining students will be turned away, and will have to make thier own way to school via public transport. 

With NTU adopting a mixed-based learning approach in AY20/21, quite a number of NTU students opted not to stay on campus with most tutorials being held on zoom and all lectures taking a web-based approach as well. 

This resulted in the increase in demand for the shuttle bus service with more students off campus. With this increase in demand, our team thought it would be a good idea to develop a booking system that helps students secure thier seats on the bus the day prior and track the demand for the bus at each location. The data collected on the demand for the buses would be then passed on to the bus company and additional buses would be sent to locations that see a huge demand. This in turn would ensure that students would be able to have a peace of mind that they would be able to board the bus and get to their lessons on time. 

## How the app works 
### User Side
1. Students would create an account at the menu page. 
    
   Example:(Matriculation No.: U1234567A , Password: Unicorn1997!)
2. At the menu page, students would also be able to reset their password. 
3. After logging in, the student would be able to make a booking for the next day's heartland shuttle buses at any of the pre-existing locations and timeslots. The student would also be able to withdraw their booking through the app. **(Note: all bookings and withdrawals have to be made before 2100hrs, no changes are allowed after that time)**

![Booking Page](https://github.com/yeldaaa/Bus-Booking-GUI/blob/main/images/main_menu.jpg)

![Booking Confirmed](https://github.com/yeldaaa/Bus-Booking-GUI/blob/main/images/booking_confirmed.jpg)

4. The student would be issued a reciept that they need to show the bus driver before being allowed on the bus.
![Reciept](https://github.com/yeldaaa/Bus-Booking-GUI/blob/main/images/receipt.jpg)

5. If the demand exceeds capacity for a certain location and timeslot, the student would be put on a waiting list and would recieve a notification in the event that a student withdraws their booking or the bus company decides to send another bus to the specified location and timeslot. The notification will be sent before 2300.

![Withdrawal](https://github.com/yeldaaa/Bus-Booking-GUI/blob/main/images/booking_withdrawn.jpg)

### Bus Company
1. The bus company will get the data from the busresponse file and if demand > 1.5x Capacity, will trigger an alert to the management. 
2. The bus company will then update if they are able to provide an additional bus to the locations that have the high demand. 
