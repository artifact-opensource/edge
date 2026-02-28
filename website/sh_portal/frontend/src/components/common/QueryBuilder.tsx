import React, { useState } from 'react';
import { PlusIcon, XMarkIcon, PlayIcon } from '@heroicons/react/24/outline';
import Button from './Button';
import Select from './Select';
import Input from './Input';
import Card, { CardHeader, CardTitle, CardDescription } from './Card';

export interface QueryCondition {
  id: string;
  field: string;
  operator: string;
  value: string;
  logicalOperator?: 'AND' | 'OR';
}

export interface QueryBuilderProps {
  fields: {
    name: string;
    label: string;
    type: 'text' | 'number' | 'date' | 'boolean';
  }[];
  onExecuteQuery?: (conditions: QueryCondition[]) => void;
  title?: string;
  description?: string;
}

const QueryBuilder: React.FC<QueryBuilderProps> = ({
  fields,
  onExecuteQuery,
  title = 'Query Builder',
  description = 'Build custom queries to analyze your data',
}) => {
  const [conditions, setConditions] = useState<QueryCondition[]>([
    {
      id: 'condition-1',
      field: fields[0]?.name || '',
      operator: 'equals',
      value: '',
      logicalOperator: 'AND',
    },
  ]);

  const operatorsByType = {
    text: [
      { label: 'Equals', value: 'equals' },
      { label: 'Not Equals', value: 'notEquals' },
      { label: 'Contains', value: 'contains' },
      { label: 'Starts With', value: 'startsWith' },
      { label: 'Ends With', value: 'endsWith' },
    ],
    number: [
      { label: 'Equals', value: 'equals' },
      { label: 'Not Equals', value: 'notEquals' },
      { label: 'Greater Than', value: 'greaterThan' },
      { label: 'Less Than', value: 'lessThan' },
      { label: 'Greater or Equal', value: 'greaterOrEqual' },
      { label: 'Less or Equal', value: 'lessOrEqual' },
    ],
    date: [
      { label: 'Equals', value: 'equals' },
      { label: 'After', value: 'after' },
      { label: 'Before', value: 'before' },
      { label: 'Between', value: 'between' },
    ],
    boolean: [
      { label: 'Is True', value: 'isTrue' },
      { label: 'Is False', value: 'isFalse' },
    ],
  };

  const addCondition = () => {
    const newCondition: QueryCondition = {
      id: `condition-${Date.now()}`,
      field: fields[0]?.name || '',
      operator: 'equals',
      value: '',
      logicalOperator: 'AND',
    };
    setConditions([...conditions, newCondition]);
  };

  const removeCondition = (id: string) => {
    setConditions(conditions.filter((c) => c.id !== id));
  };

  const updateCondition = (id: string, updates: Partial<QueryCondition>) => {
    setConditions(
      conditions.map((c) => (c.id === id ? { ...c, ...updates } : c))
    );
  };

  const handleExecute = () => {
    onExecuteQuery?.(conditions);
  };

  const getOperatorsForField = (fieldName: string) => {
    const field = fields.find((f) => f.name === fieldName);
    if (!field) return operatorsByType.text;
    return operatorsByType[field.type] || operatorsByType.text;
  };

  const getFieldType = (fieldName: string) => {
    return fields.find((f) => f.name === fieldName)?.type || 'text';
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>{title}</CardTitle>
            <CardDescription>{description}</CardDescription>
          </div>
          <Button
            variant="primary"
            size="sm"
            onClick={handleExecute}
            leftIcon={<PlayIcon className="h-4 w-4" />}
            disabled={conditions.length === 0 || conditions.some((c) => !c.value)}
          >
            Execute Query
          </Button>
        </div>
      </CardHeader>

      <div className="space-y-3">
        {conditions.map((condition, index) => (
          <div key={condition.id}>
            {/* Logical Operator */}
            {index > 0 && (
              <div className="mb-2 flex items-center gap-2">
                <div className="h-px flex-1 bg-gray-200" />
                <Select
                  value={condition.logicalOperator}
                  onChange={(e) =>
                    updateCondition(condition.id, {
                      logicalOperator: e.target.value as 'AND' | 'OR',
                    })
                  }
                  className="w-24"
                >
                  <option value="AND">AND</option>
                  <option value="OR">OR</option>
                </Select>
                <div className="h-px flex-1 bg-gray-200" />
              </div>
            )}

            {/* Condition */}
            <div className="flex items-start gap-2 rounded-lg border border-gray-200 bg-gray-50 p-3">
              <div className="flex-1 space-y-2">
                <div className="grid grid-cols-3 gap-2">
                  {/* Field */}
                  <Select
                    value={condition.field}
                    onChange={(e) => {
                      const fieldType = getFieldType(e.target.value);
                      const operators = operatorsByType[fieldType as keyof typeof operatorsByType];
                      updateCondition(condition.id, {
                        field: e.target.value,
                        operator: operators[0].value,
                      });
                    }}
                  >
                    {fields.map((field) => (
                      <option key={field.name} value={field.name}>
                        {field.label}
                      </option>
                    ))}
                  </Select>

                  {/* Operator */}
                  <Select
                    value={condition.operator}
                    onChange={(e) =>
                      updateCondition(condition.id, { operator: e.target.value })
                    }
                  >
                    {getOperatorsForField(condition.field).map((op) => (
                      <option key={op.value} value={op.value}>
                        {op.label}
                      </option>
                    ))}
                  </Select>

                  {/* Value */}
                  {condition.operator !== 'isTrue' && condition.operator !== 'isFalse' && (
                    <Input
                      type={
                        getFieldType(condition.field) === 'number'
                          ? 'number'
                          : getFieldType(condition.field) === 'date'
                          ? 'date'
                          : 'text'
                      }
                      value={condition.value}
                      onChange={(e) =>
                        updateCondition(condition.id, { value: e.target.value })
                      }
                      placeholder="Value..."
                    />
                  )}
                </div>
              </div>

              {/* Remove Button */}
              {conditions.length > 1 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => removeCondition(condition.id)}
                  aria-label="Remove condition"
                >
                  <XMarkIcon className="h-5 w-5" />
                </Button>
              )}
            </div>
          </div>
        ))}

        {/* Add Condition */}
        <Button variant="secondary" size="sm" onClick={addCondition} leftIcon={<PlusIcon className="h-4 w-4" />}>
          Add Condition
        </Button>
      </div>

      {/* Query Preview */}
      <div className="mt-4 rounded-md bg-gray-900 p-4">
        <p className="mb-2 text-xs font-medium uppercase tracking-wider text-gray-400">
          Query Preview
        </p>
        <code className="text-sm text-green-400">
          {conditions.length === 0 ? (
            'No conditions'
          ) : (
            <>
              SELECT * FROM data WHERE{' '}
              {conditions.map((c, i) => (
                <span key={c.id}>
                  {i > 0 && <span className="text-blue-400"> {c.logicalOperator} </span>}
                  <span className="text-yellow-400">{c.field}</span>{' '}
                  <span className="text-purple-400">{c.operator}</span>{' '}
                  {c.operator !== 'isTrue' && c.operator !== 'isFalse' && (
                    <span className="text-green-400">'{c.value || '?'}'</span>
                  )}
                </span>
              ))}
            </>
          )}
        </code>
      </div>
    </Card>
  );
};

export default QueryBuilder;
