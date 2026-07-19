// components/patient/DrugInteractionModal.tsx - Full-screen severe interaction alert

'use client';

import { DrugInteraction } from '@/lib/types';
import { useState } from 'react';

interface DrugInteractionModalProps {
  interactions: DrugInteraction[];
  onClose: () => void;
  onCallDoctor?: () => void;
}

export function DrugInteractionModal({
  interactions,
  onClose,
  onCallDoctor,
}: DrugInteractionModalProps) {
  const [acknowledgedRisks, setAcknowledgedRisks] = useState(false);

  if (!interactions || interactions.length === 0) {
    return null;
  }

  const primaryInteraction = interactions[0];
  const isSevere = primaryInteraction.severity === 'severe';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black bg-opacity-75" onClick={onClose}></div>

      {/* Modal */}
      <div className={`relative w-full max-w-2xl rounded-xl shadow-2xl overflow-hidden animate-in ${
        isSevere ? 'bg-red-50 border-4 border-red-500' : 'bg-yellow-50 border-4 border-yellow-500'
      }`}>
        {/* Header */}
        <div className={`p-6 ${isSevere ? 'bg-red-600' : 'bg-yellow-600'}`}>
          <div className="flex items-center gap-4">
            <span className="text-5xl">{isSevere ? '⚠️' : '⚡'}</span>
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-white mb-1">
                {isSevere ? 'SERIOUS' : 'IMPORTANT'} Drug Interaction
              </h1>
              <p className="text-white text-sm opacity-90">
                {isSevere ? 'Do not combine these medications' : 'Monitor this combination closely'}
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 text-3xl p-2 hover:bg-white/20 rounded-lg transition"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-8 space-y-6">
          {/* Primary Interaction */}
          <div className="bg-white rounded-lg p-6 border-2 border-gray-200">
            <h2 className={`text-2xl font-bold mb-4 ${
              isSevere ? 'text-red-900' : 'text-yellow-900'
            }`}>
              {primaryInteraction.interaction_name || 'Medication Interaction'}
            </h2>

            <div className="space-y-4">
              <div>
                <p className="text-sm font-semibold text-gray-600 mb-2">Clinical Effect:</p>
                <p className="text-lg text-gray-900">{primaryInteraction.clinical_effect}</p>
              </div>

              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm font-semibold text-blue-900 mb-2">What This Means:</p>
                <p className="text-gray-900">{primaryInteraction.interaction_description}</p>
              </div>

              <div>
                <p className="text-sm font-semibold text-gray-600 mb-2">Management Strategy:</p>
                <p className="text-gray-900 bg-gray-50 p-4 rounded-lg">
                  {primaryInteraction.management_strategy}
                </p>
              </div>

              {primaryInteraction.monitoring_required && (
                <div className={`p-4 border-l-4 ${
                  isSevere ? 'border-red-500 bg-red-50' : 'border-yellow-500 bg-yellow-50'
                }`}>
                  <p className="text-sm font-semibold mb-2">Monitoring Required:</p>
                  <p className="text-sm text-gray-900">{primaryInteraction.monitoring_recommendations}</p>
                </div>
              )}

              {primaryInteraction.evidence_level && (
                <div>
                  <p className="text-xs text-gray-600">
                    Evidence Level: <span className="font-bold">{primaryInteraction.evidence_level}</span>
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Additional Interactions */}
          {interactions.length > 1 && (
            <div>
              <p className="text-sm font-semibold text-gray-700 mb-3">
                Additional Interactions ({interactions.length - 1})
              </p>
              <div className="space-y-2 max-h-40 overflow-y-auto">
                {interactions.slice(1).map((interaction, idx) => (
                  <div key={idx} className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                    <p className="text-sm font-semibold text-gray-900">
                      {interaction.interaction_name || 'Drug Interaction'}
                    </p>
                    <p className="text-xs text-gray-600 mt-1">{interaction.clinical_effect}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Risk Acknowledgment */}
          <div className="flex items-start gap-3 p-4 bg-gray-100 rounded-lg">
            <input
              type="checkbox"
              id="acknowledge"
              checked={acknowledgedRisks}
              onChange={(e) => setAcknowledgedRisks(e.target.checked)}
              className="w-5 h-5 mt-1 rounded border-gray-300 accent-blue-600 cursor-pointer"
            />
            <label htmlFor="acknowledge" className="text-sm text-gray-900 cursor-pointer flex-1">
              I understand the risks of this drug combination and have discussed this with my doctor
            </label>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4 pt-6">
            <button
              onClick={onCallDoctor}
              className={`flex-1 px-6 py-3 rounded-lg font-semibold text-white transition ${
                isSevere
                  ? 'bg-red-600 hover:bg-red-700'
                  : 'bg-yellow-600 hover:bg-yellow-700'
              }`}
            >
              📞 Contact My Doctor
            </button>
            <button
              onClick={onClose}
              disabled={isSevere && !acknowledgedRisks}
              className="flex-1 px-6 py-3 rounded-lg font-semibold bg-gray-300 text-gray-900 hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              I Understand
            </button>
          </div>

          {isSevere && !acknowledgedRisks && (
            <p className="text-center text-xs text-gray-600">
              Please acknowledge you understand the risks before proceeding
            </p>
          )}
        </div>

        {/* Footer Message */}
        <div className="bg-gray-100 px-8 py-4 text-center">
          <p className="text-xs text-gray-700">
            This is not medical advice. Always consult your doctor before making medication changes.
          </p>
        </div>
      </div>
    </div>
  );
}
