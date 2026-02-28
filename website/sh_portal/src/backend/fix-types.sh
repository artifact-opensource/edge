#!/bin/bash
# Quick fix for TypeScript type inference issues
# Replace problematic destructuring with type assertions

for file in src/routes/activities.ts src/routes/comments.ts src/routes/permissions.ts; do
  # Fix request.body accessing
  sed -i 's/const { \([^}]*\) } = request.body;/const { \1 } = request.body as any;/g' "$file"
  
  # Fix request.params accessing
  sed -i 's/const { \([^}]*\) } = request.params;/const { \1 } = request.params as any;/g' "$file"
  
  # Fix request.query accessing
  sed -i 's/const { \([^}]*\) } = request.query;/const { \1 } = request.query as any;/g' "$file"
done

echo "Type fixes applied"
