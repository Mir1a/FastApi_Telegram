PGDMP  7            	        |           postgres    10.23    16.0                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    12938    postgres    DATABASE     |   CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE postgres;
                postgres    false                      0    66596    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public          postgres    false    197   	                 0    66639    request_logs 
   TABLE DATA           X   COPY public.request_logs (id, user_id, bottoken, chatid, message, response) FROM stdin;
    public          postgres    false    203   9	                 0    66603    roles 
   TABLE DATA           )   COPY public.roles (id, name) FROM stdin;
    public          postgres    false    199   |
                 0    66617    users 
   TABLE DATA           �   COPY public.users (id, username, role_id, hashed_password, is_active, is_superuser, is_verified, manager_id, email) FROM stdin;
    public          postgres    false    201   �
                   0    0    request_logs_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.request_logs_id_seq', 3, true);
          public          postgres    false    202            !           0    0    roles_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.roles_id_seq', 3, true);
          public          postgres    false    198            "           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 6, true);
          public          postgres    false    200                  x�K567N4J66KMK����� .:C         3  x��P�K�0~n��r�Uڴ%[߆���D|J�^�����t���廉�(�������K=cI��	�A�!�Ec0$�T��B��(�BS���-��6��}[��3/�0�J��M��1b��&O9O�$�����bq��ǧ�^N���z�j��������a��ˢ9g�E�gw��5�/	-�����~Y,d9KB�I��?���)6���ג�-Z�\�ǦC�z���[;(j�Ӣ7�ʝ�?ܿ>'d+IR��A��-;g�݄�t#���;�aq�F�c�yƓ��<9I����z���'Q���         $   x�3�,-N-�2��M�KL��9Sr3�b���� �y         �  x���I��PF��;�Yax�Ƈ�@��P�"�c��)��c:)�*�t��[|������[�WR����cIpv�p�V׭hp���4��/X��\H:b'g�$ic(�@��J]�DO�·��K
�<��69V ��ӄ��r"�"/������\X�!b�D��\��j]���w�i�-�.po��H�b�}`�Q�������g6)��l��NYs7P�n��Ä*��C=xi�7��1���HH����1z)��~>C�6wlR�%�wWhE�7���m���Uͨ��q�]1��z������[��0ɱ5Ly� ��%Q�U���
��x��5�.�t˟�<>��L���5J�7���fa�
��`�������A}�+��W|��<�KT�	�?	� 0���Q���|�r��_(T<E�4ʥ���X�D�b��[f�,eF�4dɰ+�BOp�&I�)��%     