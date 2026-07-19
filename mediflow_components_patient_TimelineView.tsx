// components/patient/TimelineView.tsx - Enhanced visual timeline with colors and relationships

'use client';

import { TimelineEvent, EventType, EventSeverity } from '@/lib/types';
import { useState } from 'react';

interface TimelineViewProps {
  events: TimelineEvent[];
  isLoading?: boolean;
  error?: string | null;
}

const eventTypeColors = {
  medication: 'bg-blue-500',
  lab: 'bg-green-500',
  appointment: 'bg-purple-500',
  vital: 'bg-orange-500',
  note: 'bg-indigo-500',
  procedure: 'bg-pink-500',
};

const eventTypeIcons = {
  medication: '💊',
  lab: '🧪',
  appointment: '📅',
  vital: '❤️',
  note: '📝',
  procedure: '🏥',
};

const severityColors = {
  critical: 'text-red-600 bg-red-50',
  high: 'text-orange-600 bg-orange-50',
  medium: 'text-yellow-600 bg-yellow-50',
  low: 'text-blue-600 bg-blue-50',
  info: 'text-gray-600 bg-gray-50',
};

export function TimelineView({ events, isLoading, error }: TimelineViewProps) {
  const [selectedEvent, setSelectedEvent] = useState<TimelineEvent | null>(null);
  const [expandedEventId, setExpandedEventId] = useState<string | null>(null);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p className="ml-4 text-gray-600">Loading your health timeline...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
        <p className="font-semibold">Error loading timeline</p>
        <p className="text-sm">{error}</p>
      </div>
    );
  }

  if (!events || events.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600 mb-4">No health events yet</p>
        <p className="text-sm text-gray-500">Upload medical documents to start building your timeline</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Timeline Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Your Health Timeline</h2>
        <p className="text-sm text-gray-600 mt-1">
          {events.length} event{events.length !== 1 ? 's' : ''} • Most recent first
        </p>
      </div>

      {/* Timeline Container */}
      <div className="relative">
        {/* Vertical line */}
        <div className="absolute left-6 top-0 bottom-0 w-1 bg-gradient-to-b from-blue-400 to-purple-400"></div>

        {/* Timeline Events */}
        <div className="space-y-6">
          {events.map((event, index) => (
            <div key={event.id} className="relative">
              {/* Timeline dot */}
              <div
                className={`absolute left-0 top-2 w-12 h-12 rounded-full flex items-center justify-center text-2xl border-4 border-white shadow-md cursor-pointer transition-transform hover:scale-110 ${
                  eventTypeColors[event.event_type]
                }`}
              >
                {eventTypeIcons[event.event_type]}
              </div>

              {/* Event card */}
              <div
                onClick={() => setSelectedEvent(event)}
                className={`ml-24 p-4 rounded-lg border-2 cursor-pointer transition-all hover:shadow-lg ${
                  expandedEventId === event.id
                    ? 'bg-blue-50 border-blue-400 shadow-lg'
                    : 'bg-white border-gray-200 hover:border-blue-300'
                }`}
              >
                {/* Event Header */}
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-bold text-gray-900 flex items-center gap-2">
                      {event.title}
                      {event.is_abnormal && (
                        <span className="text-xs font-bold text-white bg-red-500 px-2 py-1 rounded">
                          ⚠️ ABNORMAL
                        </span>
                      )}
                    </h3>
                    <p className="text-xs text-gray-500 mt-1">
                      {new Date(event.event_date).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric',
                      })}
                    </p>
                  </div>
                  <span
                    className={`text-xs font-bold px-3 py-1 rounded-full ${severityColors[event.severity]}`}
                  >
                    {event.severity.toUpperCase()}
                  </span>
                </div>

                {/* Event Description */}
                {event.description && (
                  <p className="text-sm text-gray-700 mb-3">{event.description}</p>
                )}

                {/* Clinical Insight */}
                {event.clinical_insight && (
                  <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg mb-3">
                    <p className="text-xs font-semibold text-blue-900 mb-1">💡 AI Insight</p>
                    <p className="text-sm text-blue-800">{event.clinical_insight}</p>
                  </div>
                )}

                {/* Related Events */}
                {event.related_event_ids.length > 0 && (
                  <div className="text-xs text-gray-600 pt-2 border-t">
                    <p className="font-semibold mb-1">Related Events: {event.related_event_ids.length}</p>
                    <p className="text-gray-500">
                      Events linked by date, diagnosis, or treatment pattern
                    </p>
                  </div>
                )}

                {/* Expand Button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setExpandedEventId(expandedEventId === event.id ? null : event.id);
                  }}
                  className="mt-3 text-sm text-blue-600 hover:text-blue-800 font-semibold"
                >
                  {expandedEventId === event.id ? '▼ Collapse' : '► More Details'}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Selected Event Modal */}
      {selectedEvent && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedEvent(null)}
        >
          <div
            className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-2xl font-bold text-gray-900">{selectedEvent.title}</h2>
              <button
                onClick={() => setSelectedEvent(null)}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600">Date</p>
                <p className="font-semibold text-gray-900">
                  {new Date(selectedEvent.event_date).toLocaleDateString('en-US', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </p>
              </div>

              <div>
                <p className="text-sm text-gray-600">Type</p>
                <p className="font-semibold text-gray-900 capitalize">{selectedEvent.event_type}</p>
              </div>

              {selectedEvent.description && (
                <div>
                  <p className="text-sm text-gray-600">Description</p>
                  <p className="text-gray-900">{selectedEvent.description}</p>
                </div>
              )}

              {selectedEvent.clinical_insight && (
                <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <p className="text-sm font-semibold text-blue-900 mb-2">💡 Clinical Insight</p>
                  <p className="text-gray-900">{selectedEvent.clinical_insight}</p>
                </div>
              )}

              <div>
                <p className="text-sm text-gray-600">Status</p>
                <p className={`font-semibold px-3 py-1 rounded-full inline-block ${severityColors[selectedEvent.severity]}`}>
                  {selectedEvent.severity.toUpperCase()}
                </p>
              </div>

              {selectedEvent.is_abnormal && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-sm font-semibold text-red-900">⚠️ Abnormal Finding</p>
                  <p className="text-sm text-red-800 mt-1">This value is outside the normal range. Discuss with your doctor.</p>
                </div>
              )}
            </div>

            <button
              onClick={() => setSelectedEvent(null)}
              className="mt-6 w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
