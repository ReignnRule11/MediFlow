// components/patient/MedicationCard.tsx - Medication display component

'use client';

import { Medication, DrugInteraction } from '@/lib/types';
import { useState } from 'react';

interface MedicationCardProps {
  medication: Medication;
  interactions?: DrugInteraction[];
  onRefill?: (medicationId: string) => void;
  onViewDetails?: (medicationId: string) => void;
}

interface MedicationCardProps {
  medication: Medication;
  interactions?: DrugInteraction[];
  onRefill?: (medicationId: string) => void;
  onViewDetails?: (medicationId: string) => void;
  onShowInteractionModal?: (interactions: DrugInteraction[]) => void;
}

export function MedicationCard({
  medication,
  interactions = [],
  onRefill,
  onViewDetails,
  onShowInteractionModal,
}: MedicationCardProps) {
  const [showDetails, setShowDetails] = useState(false);
  const [showInteractionModal, setShowInteractionModal] = useState(false);

  const hasInteractions = interactions.length > 0;
  const severeInteractions = interactions.filter(i => i.severity === 'severe');
  const moderateInteractions = interactions.filter(i => i.severity === 'moderate');

  const statusColors = {
    active: 'bg-green-100 text-green-800',
    discontinued: 'bg-gray-100 text-gray-800',
    paused: 'bg-yellow-100 text-yellow-800',
    completed: 'bg-blue-100 text-blue-800',
  };

  const adherenceColor = medication.adherence_score >= 0.8 ? 'text-green-600' : 
                        medication.adherence_score >= 0.5 ? 'text-yellow-600' : 'text-red-600';

  // Handler for severe interaction click - opens full modal
  const handleSevereInteractionClick = () => {
    setShowInteractionModal(true);
    onShowInteractionModal?.(severeInteractions);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-bold text-gray-900">{medication.name}</h3>
          {medication.generic_name && medication.generic_name !== medication.name && (
            <p className="text-sm text-gray-600">Generic: {medication.generic_name}</p>
          )}
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColors[medication.status]}`}>
          {medication.status.charAt(0).toUpperCase() + medication.status.slice(1)}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
        <div>
          <p className="text-gray-600">Strength</p>
          <p className="font-medium text-gray-900">{medication.strength}</p>
        </div>
        <div>
          <p className="text-gray-600">Frequency</p>
          <p className="font-medium text-gray-900">{medication.frequency}</p>
        </div>
        <div>
          <p className="text-gray-600">Start Date</p>
          <p className="font-medium text-gray-900">
            {new Date(medication.start_date).toLocaleDateString()}
          </p>
        </div>
        <div>
          <p className="text-gray-600">Adherence</p>
          <p className={`font-medium ${adherenceColor}`}>
            {Math.round(medication.adherence_score * 100)}%
          </p>
        </div>
      </div>

      {severeInteractions.length > 0 && (
        <div 
          onClick={handleSevereInteractionClick}
          className="mb-4 p-4 bg-red-100 border-2 border-red-500 rounded-lg cursor-pointer hover:bg-red-50 transition-colors"
        >
          <p className="text-lg font-bold text-red-900 mb-2">⚠️ SEVERE DRUG INTERACTION</p>
          <p className="text-sm text-red-800 mb-3">
            {severeInteractions.length} serious interaction{severeInteractions.length !== 1 ? 's' : ''} detected
          </p>
          <p className="text-xs text-red-700">
            {severeInteractions[0].description}
          </p>
          <button
            onClick={(e) => {
              e.stopPropagation();
              handleSevereInteractionClick();
            }}
            className="mt-3 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-semibold text-sm"
          >
            View Interaction Details
          </button>
        </div>
      )}

      {moderateInteractions.length > 0 && !severeInteractions.length && (
        <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm font-semibold text-yellow-800 mb-1">⚠️ Moderate Interactions</p>
          <p className="text-xs text-yellow-700">
            {moderateInteractions.length} potential interaction{moderateInteractions.length !== 1 ? 's' : ''} to monitor
          </p>
        </div>
      )}

      <div className="flex gap-2 pt-4 border-t">
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="flex-1 px-3 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 text-sm font-medium transition-colors"
        >
          {showDetails ? 'Hide Details' : 'View Details'}
        </button>

        {medication.refills_remaining > 0 && onRefill && (
          <button
            onClick={() => onRefill(medication.id)}
            className="flex-1 px-3 py-2 bg-green-50 text-green-600 rounded-lg hover:bg-green-100 text-sm font-medium transition-colors"
          >
            Request Refill
          </button>
        )}

        {medication.refills_remaining === 0 && (
          <div className="flex-1 px-3 py-2 bg-gray-50 text-gray-600 rounded-lg text-sm font-medium text-center">
            No Refills
          </div>
        )}
      </div>

      {showDetails && (
        <div className="mt-4 pt-4 border-t space-y-3">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-gray-600">Dosage Form</p>
              <p className="font-medium text-gray-900">{medication.dosage_form}</p>
            </div>
            <div>
              <p className="text-gray-600">Refills Remaining</p>
              <p className="font-medium text-gray-900">{medication.refills_remaining}</p>
            </div>
          </div>

          {medication.end_date && (
            <div>
              <p className="text-gray-600 text-sm">End Date</p>
              <p className="font-medium text-gray-900">
                {new Date(medication.end_date).toLocaleDateString()}
              </p>
            </div>
          )}

          <button
            onClick={() => onViewDetails?.(medication.id)}
            className="w-full mt-3 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium transition-colors"
          >
            View Full Details & Instructions
          </button>
        </div>
      )}
    </div>
  );
}
