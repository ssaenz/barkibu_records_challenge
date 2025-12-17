import React, { useEffect, useState } from 'react';
import { MedicalRecord, Visit } from '../types';
import { Stethoscope, User, Calendar, Plus, Trash2 } from 'lucide-react';

interface MedicalRecordEditorProps {
  initialData?: MedicalRecord;
  onSave?: (data: MedicalRecord) => void;
}

export const MedicalRecordEditor: React.FC<MedicalRecordEditorProps> = ({ initialData, onSave }) => {
  const [data, setData] = useState<MedicalRecord>(initialData || {});

  useEffect(() => {
    if (initialData) {
      setData(initialData);
    }
  }, [initialData]);

  const updatePetInfo = (field: string, value: string) => {
    const newData = { ...data, pet_info: { ...data.pet_info, [field]: value } };
    setData(newData);
    onSave?.(newData);
  };

  const updateVetInfo = (field: string, value: string) => {
    const newData = { ...data, veterinary_info: { ...data.veterinary_info, [field]: value } };
    setData(newData);
    onSave?.(newData);
  };

  const updateVisit = (index: number, field: keyof Visit, value: string) => {
    const newVisits = [...(data.visits || [])];
    newVisits[index] = { ...newVisits[index], [field]: value };
    const newData = { ...data, visits: newVisits };
    setData(newData);
    onSave?.(newData);
  };

  const addVisit = () => {
    const newData = { ...data, visits: [...(data.visits || []), {}] };
    setData(newData);
    onSave?.(newData);
  };

  const removeVisit = (index: number) => {
    const newVisits = [...(data.visits || [])];
    newVisits.splice(index, 1);
    const newData = { ...data, visits: newVisits };
    setData(newData);
    onSave?.(newData);
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 h-full overflow-y-auto">
      <div className="flex items-center gap-2 mb-6 pb-4 border-b">
        <Stethoscope className="w-6 h-6 text-green-600" />
        <h2 className="text-xl font-semibold text-gray-900">Medical Record</h2>
      </div>

      <div className="space-y-8">
        {/* Pet Info Section */}
        <section>
          <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider mb-4 flex items-center gap-2">
            <User className="w-4 h-4" /> Pet Information
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
              <input
                type="text"
                value={data.pet_info?.name || ''}
                onChange={(e) => updatePetInfo('name', e.target.value)}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                placeholder="Pet Name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Species</label>
              <input
                type="text"
                value={data.pet_info?.species || ''}
                onChange={(e) => updatePetInfo('species', e.target.value)}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                placeholder="Dog, Cat, etc."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Breed</label>
              <input
                type="text"
                value={data.pet_info?.breed || ''}
                onChange={(e) => updatePetInfo('breed', e.target.value)}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
              />
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
                <input
                  type="text"
                  value={data.pet_info?.age || ''}
                  onChange={(e) => updatePetInfo('age', e.target.value)}
                  className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Weight</label>
                <input
                  type="text"
                  value={data.pet_info?.weight || ''}
                  onChange={(e) => updatePetInfo('weight', e.target.value)}
                  className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                />
              </div>
            </div>
          </div>
        </section>

        {/* Veterinary Info Section */}
        <section>
          <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider mb-4 flex items-center gap-2">
            <Stethoscope className="w-4 h-4" /> Veterinary Clinic
          </h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Clinic Name</label>
              <input
                type="text"
                value={data.veterinary_info?.name || ''}
                onChange={(e) => updateVetInfo('name', e.target.value)}
                className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                <input
                  type="text"
                  value={data.veterinary_info?.address || ''}
                  onChange={(e) => updateVetInfo('address', e.target.value)}
                  className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                <input
                  type="text"
                  value={data.veterinary_info?.phone || ''}
                  onChange={(e) => updateVetInfo('phone', e.target.value)}
                  className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm border p-2"
                />
              </div>
            </div>
          </div>
        </section>

        {/* Visits Section */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider flex items-center gap-2">
              <Calendar className="w-4 h-4" /> Visits History
            </h3>
            <button
              onClick={addVisit}
              className="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded-full shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <Plus className="w-3 h-3 mr-1" /> Add Visit
            </button>
          </div>
          
          <div className="space-y-6">
            {data.visits?.map((visit, index) => (
              <div key={index} className="bg-gray-50 rounded-lg p-4 border border-gray-200 relative group">
                <button
                  onClick={() => removeVisit(index)}
                  className="absolute top-2 right-2 p-1 text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
                
                <div className="grid grid-cols-12 gap-4">
                  <div className="col-span-4">
                    <label className="block text-xs font-medium text-gray-500 mb-1">Date</label>
                    <input
                      type="text"
                      value={visit.date || ''}
                      onChange={(e) => updateVisit(index, 'date', e.target.value)}
                      className="w-full rounded border-gray-300 text-sm p-1.5"
                      placeholder="YYYY-MM-DD"
                    />
                  </div>
                  <div className="col-span-8">
                    <label className="block text-xs font-medium text-gray-500 mb-1">Reason</label>
                    <input
                      type="text"
                      value={visit.reason || ''}
                      onChange={(e) => updateVisit(index, 'reason', e.target.value)}
                      className="w-full rounded border-gray-300 text-sm p-1.5"
                    />
                  </div>
                  <div className="col-span-12">
                    <label className="block text-xs font-medium text-gray-500 mb-1">Diagnosis</label>
                    <textarea
                      value={visit.diagnosis || ''}
                      onChange={(e) => updateVisit(index, 'diagnosis', e.target.value)}
                      rows={2}
                      className="w-full rounded border-gray-300 text-sm p-1.5"
                    />
                  </div>
                  <div className="col-span-12">
                    <label className="block text-xs font-medium text-gray-500 mb-1">Treatment</label>
                    <textarea
                      value={visit.treatment || ''}
                      onChange={(e) => updateVisit(index, 'treatment', e.target.value)}
                      rows={2}
                      className="w-full rounded border-gray-300 text-sm p-1.5"
                    />
                  </div>
                </div>
              </div>
            ))}
            
            {(!data.visits || data.visits.length === 0) && (
              <div className="text-center py-8 text-gray-400 text-sm italic">
                No visits recorded yet.
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
};
