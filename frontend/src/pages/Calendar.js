import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import { useState, useEffect } from 'react';
import axios from 'axios';

function Calendar() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await axios.get('https://people2025.orbdent.com/appointments', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        setEvents(response.data.map(event => ({
          title: event.title,
          start: event.start_time,
          end: event.end_time,
        })));
      } catch (error) {
        console.error('Failed to fetch events');
      }
    };
    fetchEvents();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Calendar</h2>
      <div className="bg-white p-4 rounded-lg shadow-lg">
        <FullCalendar
          plugins={[dayGridPlugin]}
          initialView="dayGridMonth"
          events={events}
        />
      </div>
    </div>
  );
}

export default Calendar;
