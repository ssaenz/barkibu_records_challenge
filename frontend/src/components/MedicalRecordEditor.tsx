import React, { useEffect, useState } from 'react';
import { MedicalRecord, Visit, PhysicalExamination } from '../types';
import { Stethoscope, User, Calendar, Plus, Trash2, Activity, Pill } from 'lucide-react';

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

  const updateVisit = (index: number, field: keyof Visit, value: any) => {
    const newVisits = [...(data.visits || [])];
    newVisits[index] = { ...newVisits[index], [field]: value };
    const newData = { ...data, visits: newVisits };
    setData(newData);
    onSave?.(newData);
  };

  const updatePhysicalExam = (visitIndex: number, field: keyof PhysicalExamination, value: any) => {
    const newVisits = [...(data.visits || [])];
    const currentExam = newVisits[visitIndex].physical_examination || {};
    newVisits[visitIndex] = {
      ...newVisits[visitIndex],
      physical_examination: { ...currentExam, [field]: value }
    };
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

  // Helper to render array fields like diagnosis
  const renderStringArray = (
    visitIndex: number,
    field: 'diagnosis',
    items: string[] = [],
    label: string
  ) => (
    <div className="col-span-12">
      <label className="block text-xs font-medium text-gray-500 mb-1">{label}</label>
      {items.map((item, i) => (
        <div key={i} className="flex gap-2 mb-2">
          <input
            type="text"
            value={item}
            onChange={(e) => {
              const newItems = [...items];
              newItems[i] = e.target.value;
              updateVisit(visitIndex, field, newItems);
            }}
            className="flex-1 rounded border-gray-300 text-sm p-1.5"
          />
          <button
            onClick={() => {
              const newItems = [...items];
              newItems.splice(i, 1);
              updateVisit(visitIndex, field, newItems);
            }}
            className="text-red-500 hover:text-red-700"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      ))}
      <button
        onClick={() => updateVisit(visitIndex, field, [...items, ''])}
        className="text-xs text-blue-600 hover:text-blue-800 flex items-center gap-1"
      >
        <Plus className="w-3 h-3" /> Add {label}
      </button>
    </div>
  );

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
                  {/* Basic Visit Info */}
                  <div className="col-span-4">
                    <label className="block text-xs font-medium text-gray-500 mb-1">Date</label>
                    <input
                      type="text"
                      value={visit.visit_date || ''}
                      onChange={(e) => updateVisit(index, 'visit_date', e.target.value)}
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
                    <label className="block text-xs font-medium text-gray-500 mb-1">Anamnesis</label>
                    <textarea
                      value={visit.anamnesis || ''}
                      onChange={(e) => updateVisit(index, 'anamnesis', e.target.value)}
                      rows={2}
                      className="w-full rounded border-gray-300 text-sm p-1.5"
                    />
                  </div>

                  {/* Physical Examination */}
                  <div className="col-span-12 bg-white p-3 rounded border border-gray-100">
                    <h4 className="text-xs font-semibold text-gray-700 mb-2 flex items-center gap-1">
                      <Activity className="w-3 h-3" /> Physical Examination
                    </h4>
                    <div className="grid grid-cols-3 gap-3">
                      <div>
                        <label className="block text-[10px] font-medium text-gray-500 mb-1">Weight (kg)</label>
                        <input
                          type="number"
                          value={visit.physical_examination?.weight || ''}
                          onChange={(e) => updatePhysicalExam(index, 'weight', parseFloat(e.target.value))}
                          className="w-full rounded border-gray-300 text-sm p-1"
                        />
                      </div>
                      <div>
                        <label className="block text-[10px] font-medium text-gray-500 mb-1">Temp (°C)</label>
                        <input
                          type="number"
                          value={visit.physical_examination?.temperature || ''}
                          onChange={(e) => updatePhysicalExam(index, 'temperature', parseFloat(e.target.value))}
                          className="w-full rounded border-gray-300 text-sm p-1"
                        />
                      </div>
                      <div>
                        <label className="block text-[10px] font-medium text-gray-500 mb-1">Heart Rate</label>
                        <input
                          type="number"
                          value={visit.physical_examination?.heart_rate || ''}
                          onChange={(e) => updatePhysicalExam(index, 'heart_rate', parseFloat(e.target.value))}
                          className="w-full rounded border-gray-300 text-sm p-1"
                        />
                      </div>
                      <div className="col-span-3">
                        <label className="block text-[10px] font-medium text-gray-500 mb-1">Findings</label>
                        <textarea
                          value={visit.physical_examination?.findings?.join('\n') || ''}
                          onChange={(e) => updatePhysicalExam(index, 'findings', e.target.value.split('\n'))}
                          rows={2}
                          className="w-full rounded border-gray-300 text-sm p-1"
                          placeholder="One finding per line"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Diagnosis */}
                  {renderStringArray(index, 'diagnosis', visit.diagnosis, 'Diagnosis')}

                  {/* Treatment / Medications */}
                  <div className="col-span-12">
                    <label className="block text-xs font-medium text-gray-500 mb-1 flex items-center gap-1">
                      <Pill className="w-3 h-3" /> Treatment / Medications
                    </label>
                    {visit.treatment?.map((med, medIndex) => (
                      <div key={medIndex} className="flex gap-2 mb-2 items-start bg-blue-50 p-2 rounded">
                        <div className="grid grid-cols-2 gap-2 flex-1">
                          <input
                            placeholder="Name"
                            value={med.name}
                            onChange={(e) => {
                              const newTreatment = [...(visit.treatment || [])];
                              newTreatment[medIndex] = { ...med, name: e.target.value };
                              updateVisit(index, 'treatment', newTreatment);
                            }}
                            className="rounded border-gray-300 text-xs p-1"
                          />
                          <input
                            placeholder="Dosage"
                            value={med.dosage || ''}
                            onChange={(e) => {
                              const newTreatment = [...(visit.treatment || [])];
                              newTreatment[medIndex] = { ...med, dosage: e.target.value };
                              updateVisit(index, 'treatment', newTreatment);
                            }}
                            className="rounded border-gray-300 text-xs p-1"
                          />
                        </div>
                        <button
                          onClick={() => {
                            const newTreatment = [...(visit.treatment || [])];
                            newTreatment.splice(medIndex, 1);
                            updateVisit(index, 'treatment', newTreatment);
                          }}
                          className="text-red-500 hover:text-red-700 mt-1"
                        >
                          <Trash2 className="w-3 h-3" />
                        </button>
                      </div>
                    ))}
                    <button
                      onClick={() => updateVisit(index, 'treatment', [...(visit.treatment || []), { name: '' }])}
                      className="text-xs text-blue-600 hover:text-blue-800 flex items-center gap-1"
                    >
                      <Plus className="w-3 h-3" /> Add Medication
                    </button>
                  </div>

                  <div className="col-span-12">
                    <label className="block text-xs font-medium text-gray-500 mb-1">Plan</label>
                    <textarea
                      value={visit.plan || ''}
                      onChange={(e) => updateVisit(index, 'plan', e.target.value)}
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
