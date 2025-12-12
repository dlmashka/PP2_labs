-- ===================================================
-- LAB 11: Stored Procedures and Functions
-- PhoneBook Database
-- ===================================================

-- ===== 1. CREATE TABLE (if not exists) =====
CREATE TABLE IF NOT EXISTS PhoneBook (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  phone TEXT,
  CONSTRAINT phonebook_name_unique UNIQUE (name)
);

-- ===== 2. FUNCTION: search_contacts =====
-- Returns all records based on a pattern (name, surname, or phone number)
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, name TEXT, phone TEXT) AS $$
BEGIN
  RETURN QUERY
  SELECT pb.id, pb.name, pb.phone
  FROM PhoneBook pb
  WHERE pb.name ILIKE '%' || pattern || '%'
     OR pb.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- ===== 3. PROCEDURE: add_or_update_user =====
-- Insert new user by name and phone, update phone if user already exists
CREATE OR REPLACE PROCEDURE add_or_update_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO PhoneBook(name, phone)
  VALUES (p_name, p_phone)
  ON CONFLICT (name)
  DO UPDATE SET phone = EXCLUDED.phone;
  
  RAISE NOTICE 'User % processed successfully', p_name;
END;
$$;

-- ===== 4. PROCEDURE: add_many_users =====
-- Insert many new users from list of name and phone
-- Uses loop and if statement to check phone correctness (regex: at least 5 digits)
-- Returns all incorrect data via RAISE NOTICE
CREATE OR REPLACE PROCEDURE add_many_users(users_json JSON)
LANGUAGE plpgsql AS $$
DECLARE
  elem JSON;
  u_name TEXT;
  u_phone TEXT;
  invalids TEXT := '';
  valid_count INT := 0;
  invalid_count INT := 0;
BEGIN
  -- Loop through JSON array elements
  FOR elem IN SELECT * FROM json_array_elements(users_json)
  LOOP
    u_name := elem->>'name';
    u_phone := elem->>'phone';
    
    -- Check phone correctness: must have at least 5 digits
    IF u_phone IS NOT NULL AND u_phone ~ '^\d{5,}$' THEN
      -- Valid phone: insert or update (UPSERT)
      CALL add_or_update_user(u_name, u_phone);
      valid_count := valid_count + 1;
    ELSE
      -- Invalid phone: collect in string
      invalids := invalids || format('Name: %s, Phone: %s; ', u_name, COALESCE(u_phone,'NULL'));
      invalid_count := invalid_count + 1;
    END IF;
  END LOOP;

  -- Return summary
  RAISE NOTICE 'Batch processing completed. Valid: %, Invalid: %', valid_count, invalid_count;
  
  IF invalids <> '' THEN
    RAISE NOTICE 'Incorrect entries: %', invalids;
  END IF;
END;
$$;

-- ===== 5. FUNCTION: get_contacts_paginated =====
-- Query data from tables with pagination (by limit and offset)
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name TEXT, phone TEXT) AS $$
BEGIN
  -- Validate pagination parameters
  IF p_limit IS NULL OR p_limit <= 0 THEN
    RAISE EXCEPTION 'Limit must be greater than 0';
  END IF;
  
  IF p_offset IS NULL OR p_offset < 0 THEN
    RAISE EXCEPTION 'Offset must be non-negative';
  END IF;
  
  RETURN QUERY
  SELECT pb.id, pb.name, pb.phone
  FROM PhoneBook pb
  ORDER BY pb.id
  LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- ===== 6. PROCEDURE: delete_user =====
-- Delete data from tables by username or phone
-- At least one parameter must be provided
CREATE OR REPLACE PROCEDURE delete_user(p_name TEXT DEFAULT NULL, p_phone TEXT DEFAULT NULL)
LANGUAGE plpgsql AS $$
DECLARE
  deleted_count INT := 0;
BEGIN
  -- Validate: at least one parameter must be provided
  IF p_name IS NULL AND p_phone IS NULL THEN
    RAISE EXCEPTION 'At least one parameter (name or phone) must be provided for deletion';
  END IF;

  -- Delete records matching name or phone
  DELETE FROM PhoneBook
  WHERE (p_name IS NOT NULL AND name = p_name)
     OR (p_phone IS NOT NULL AND phone = p_phone);
  
  -- Get number of deleted rows
  GET DIAGNOSTICS deleted_count = ROW_COUNT;
  
  RAISE NOTICE 'Deleted % row(s) from PhoneBook', deleted_count;
END;
$$;

-- ===== 7. ADDITIONAL UTILITY FUNCTION: get_contact_count =====
-- Returns total number of contacts (useful for pagination)
CREATE OR REPLACE FUNCTION get_contact_count()
RETURNS INT AS $$
DECLARE
  count INT;
BEGIN
  SELECT COUNT(*) INTO count FROM PhoneBook;
  RETURN count;
END;
$$ LANGUAGE plpgsql;

-- ===== 8. TEST DATA =====
-- Uncomment to load test data (optional)
/*
INSERT INTO PhoneBook (name, phone) VALUES
  ('Ali', '77001234567'),
  ('Bob', '77001230000'),
  ('Charlie', '87777778888'),
  ('Diana', '77123456789')
ON CONFLICT (name) DO NOTHING;
*/

-- ===== QUERIES FOR TESTING =====
-- Test search function:
-- SELECT * FROM search_contacts('Ali');
-- SELECT * FROM search_contacts('77');

-- Test pagination function:
-- SELECT * FROM get_contacts_paginated(2, 0);
-- SELECT * FROM get_contacts_paginated(2, 2);

-- Test add/update procedure:
-- CALL add_or_update_user('Eva', '77999999999');

-- Test batch insert:
-- CALL add_many_users('[
--   {"name": "Frank", "phone": "77555555555"},
--   {"name": "Grace", "phone": "123"},
--   {"name": "Ali", "phone": "77001234567"}
-- ]'::json);

-- Test delete procedure:
-- CALL delete_user(p_name => 'Eva');
-- CALL delete_user(p_phone => '77555555555');

-- View all contacts:
-- SELECT * FROM PhoneBook ORDER BY id;

-- Get contact count:
-- SELECT get_contact_count() as total_contacts;
