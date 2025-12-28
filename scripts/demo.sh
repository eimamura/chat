#!/bin/bash
# Demo script to verify end-to-end functionality

set -e

echo "=== Chat MVP Demo Script ==="
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

# List messages
echo ""
echo "4. Listing existing messages..."
MESSAGES=$(curl -s http://localhost:8000/api/messages)
MESSAGE_COUNT=$(echo "$MESSAGES" | grep -o '"id"' | wc -l)
echo -e "${GREEN}✓ Found $MESSAGE_COUNT messages${NC}"

# Create a new message
echo ""
echo "5. Creating a new message..."
CREATE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/messages \
    -H "Content-Type: application/json" \
    -d '{"username":"DemoUser","content":"Hello from demo script '$(date +%s)'"}')
if echo "$CREATE_RESPONSE" | grep -q '"id"'; then
    NEW_MESSAGE_ID=$(echo "$CREATE_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
    echo -e "${GREEN}✓ Message created successfully (ID: $NEW_MESSAGE_ID)${NC}"
else
    echo -e "${RED}✗ Failed to create message${NC}"
    echo "Response: $CREATE_RESPONSE"
    exit 1
fi

# Verify message appears in list
echo ""
echo "6. Verifying message appears in list..."
NEW_MESSAGES=$(curl -s http://localhost:8000/api/messages)
NEW_MESSAGE_COUNT=$(echo "$NEW_MESSAGES" | grep -o '"id"' | wc -l)
if [ "$NEW_MESSAGE_COUNT" -gt "$MESSAGE_COUNT" ]; then
    echo -e "${GREEN}✓ Message appears in list (count: $NEW_MESSAGE_COUNT)${NC}"
else
    echo -e "${YELLOW}⚠ Message count unchanged (expected increase)${NC}"
fi

# Delete the message
echo ""
echo "7. Deleting the created message..."
DELETE_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "http://localhost:8000/api/messages/$NEW_MESSAGE_ID")
if [ "$DELETE_RESPONSE" = "204" ]; then
    echo -e "${GREEN}✓ Message deleted successfully${NC}"
else
    echo -e "${RED}✗ Failed to delete message (HTTP $DELETE_RESPONSE)${NC}"
    exit 1
fi

# Verify message is removed
echo ""
echo "8. Verifying message is removed from list..."
FINAL_MESSAGES=$(curl -s http://localhost:8000/api/messages)
FINAL_MESSAGE_COUNT=$(echo "$FINAL_MESSAGES" | grep -o '"id"' | wc -l)
if [ "$FINAL_MESSAGE_COUNT" -eq "$MESSAGE_COUNT" ]; then
    echo -e "${GREEN}✓ Message removed from list (count: $FINAL_MESSAGE_COUNT)${NC}"
else
    echo -e "${YELLOW}⚠ Message count mismatch (expected: $MESSAGE_COUNT, got: $FINAL_MESSAGE_COUNT)${NC}"
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
echo "Access the chat application:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "Try the chat:"
echo "  1. Open http://localhost:3000 in your browser"
echo "  2. Enter a username"
echo "  3. Send messages and see them appear in real-time!"

