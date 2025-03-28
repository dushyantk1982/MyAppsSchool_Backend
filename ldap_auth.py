# import ldap
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# LDAP_SERVER = os.getenv("LDAP_SERVER")
# LDAP_BASE_DN = os.getenv("LDAP_BASE_DN")
# LDAP_USER_DN = os.getenv("LDAP_USER_DN")
# LDAP_BIND_DN = os.getenv("LDAP_BIND_DN")
# LDAP_BIND_PASSWORD = os.getenv("LDAP_BIND_PASSWORD")

# def authenticate_ldap(username: str, password: str) -> bool:
#     """
#     Authenticate user with LDAP server.
#     """
#     try:
#         # Initialize LDAP connection
#         conn = ldap.initialize(LDAP_SERVER)
#         conn.set_option(ldap.OPT_REFERRALS, 0)

#         # Bind with Admin DN
#         conn.simple_bind_s(LDAP_BIND_DN, LDAP_BIND_PASSWORD)

#         # Search for user DN
#         search_filter = f"(uid={username})"
#         search_base = f"{LDAP_USER_DN},{LDAP_BASE_DN}"
        
#         result = conn.search_s(search_base, ldap.SCOPE_SUBTREE, search_filter, ["dn"])

#         if not result:
#             return False  # User not found
        
#         user_dn = result[0][0]  # Get user's full DN
        
#         # Try to bind using the user's DN and password
#         conn.simple_bind_s(user_dn, password)
#         return True  # Authentication successful

#     except ldap.INVALID_CREDENTIALS:
#         return False
#     except ldap.LDAPError as e:
#         print("LDAP error:", e)
#         return False
#     finally:
#         conn.unbind_s()
