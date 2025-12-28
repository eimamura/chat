#!/bin/bash
# Demo script to verify end-to-end functionality

set -e

echo "=== MVP Web App Demo Script ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if services are running
echo "1. Checking if services are running..."
if ! docker compose ps | grep -q "Up"; then
    echo -e "${YELLOW}Services not running. Starting services...${NC}"
    docker compose up -d
    echo "Waiting for services to be ready..."
    sleep 10
else
    echo -e "${GREEN}✓ Services are running${NC}"
fi

# Check backend health
echo ""
echo "2. Checking backend health endpoint..."
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/healthz || echo "000")
if [ "$HEALTH_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓ Backend health check passed${NC}"
else
    echo -e "${RED}✗ Backend health check failed (HTTP $HEALTH_RESPONSE)${NC}"
    exit 1
fi

# Check API docs
echo ""
echo "3. Checking API documentation..."
DOCS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs || echo "000")
if [ "$DOCS_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓ API documentation available${NC}"
else
    echo -e "${YELLOW}⚠ API documentation not accessible (HTTP $DOCS_RESPONSE)${NC}"
fi

# List items
echo ""
echo "4. Listing existing items..."
ITEMS=$(curl -s http://localhost:8000/api/items)
ITEM_COUNT=$(echo "$ITEMS" | grep -o '"id"' | wc -l)
echo -e "${GREEN}✓ Found $ITEM_COUNT items${NC}"

# Create a new item
echo ""
echo "5. Creating a new item..."
CREATE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/items \
    -H "Content-Type: application/json" \
    -d '{"name":"Demo Item '$(date +%s)'"}')
if echo "$CREATE_RESPONSE" | grep -q '"id"'; then
    NEW_ITEM_ID=$(echo "$CREATE_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
    echo -e "${GREEN}✓ Item created successfully (ID: $NEW_ITEM_ID)${NC}"
else
    echo -e "${RED}✗ Failed to create item${NC}"
    echo "Response: $CREATE_RESPONSE"
    exit 1
fi

# Verify item appears in list
echo ""
echo "6. Verifying item appears in list..."
NEW_ITEMS=$(curl -s http://localhost:8000/api/items)
NEW_ITEM_COUNT=$(echo "$NEW_ITEMS" | grep -o '"id"' | wc -l)
if [ "$NEW_ITEM_COUNT" -gt "$ITEM_COUNT" ]; then
    echo -e "${GREEN}✓ Item appears in list (count: $NEW_ITEM_COUNT)${NC}"
else
    echo -e "${YELLOW}⚠ Item count unchanged (expected increase)${NC}"
fi

# Delete the item
echo ""
echo "7. Deleting the created item..."
DELETE_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "http://localhost:8000/api/items/$NEW_ITEM_ID")
if [ "$DELETE_RESPONSE" = "204" ]; then
    echo -e "${GREEN}✓ Item deleted successfully${NC}"
else
    echo -e "${RED}✗ Failed to delete item (HTTP $DELETE_RESPONSE)${NC}"
    exit 1
fi

# Verify item is removed
echo ""
echo "8. Verifying item is removed from list..."
FINAL_ITEMS=$(curl -s http://localhost:8000/api/items)
FINAL_ITEM_COUNT=$(echo "$FINAL_ITEMS" | grep -o '"id"' | wc -l)
if [ "$FINAL_ITEM_COUNT" -eq "$ITEM_COUNT" ]; then
    echo -e "${GREEN}✓ Item removed from list (count: $FINAL_ITEM_COUNT)${NC}"
else
    echo -e "${YELLOW}⚠ Item count mismatch (expected: $ITEM_COUNT, got: $FINAL_ITEM_COUNT)${NC}"
fi

# Check frontend
echo ""
echo "9. Checking frontend..."
FRONTEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 || echo "000")
if [ "$FRONTEND_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓ Frontend is accessible${NC}"
else
    echo -e "${YELLOW}⚠ Frontend not accessible (HTTP $FRONTEND_RESPONSE)${NC}"
fi

echo ""
echo -e "${GREEN}=== Demo completed successfully! ===${NC}"
echo ""
echo "Access the application:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"

