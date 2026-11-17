--
-- PostgreSQL database dump
--

\restrict H4MkmPKBaakhRtarqR8W0TDu5Y0qmc2ven0xfU70s1SfN3BHMnbd9jzpNoEoEs8

-- Dumped from database version 16.14
-- Dumped by pg_dump version 16.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.shop_variant DROP CONSTRAINT IF EXISTS shop_variant_product_id_ab80580a_fk_shop_product_id;
ALTER TABLE IF EXISTS ONLY public.shop_product DROP CONSTRAINT IF EXISTS shop_product_category_id_14d7eea8_fk_shop_category_id;
ALTER TABLE IF EXISTS ONLY public.shop_lot DROP CONSTRAINT IF EXISTS shop_lot_variant_id_334b69f4_fk_shop_variant_id;
ALTER TABLE IF EXISTS ONLY public.orders_statushistory DROP CONSTRAINT IF EXISTS orders_statushistory_order_id_116bfa23_fk_orders_order_id;
ALTER TABLE IF EXISTS ONLY public.orders_statushistory DROP CONSTRAINT IF EXISTS orders_statushistory_by_id_5374de9e_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.orders_shipment DROP CONSTRAINT IF EXISTS orders_shipment_order_id_661ed8ed_fk_orders_order_id;
ALTER TABLE IF EXISTS ONLY public.orders_payment DROP CONSTRAINT IF EXISTS orders_payment_order_id_bdccf250_fk_orders_order_id;
ALTER TABLE IF EXISTS ONLY public.orders_orderitemallocation DROP CONSTRAINT IF EXISTS orders_orderitemallocation_lot_id_0b86825d_fk_shop_lot_id;
ALTER TABLE IF EXISTS ONLY public.orders_orderitemallocation DROP CONSTRAINT IF EXISTS orders_orderitemallo_item_id_20193c42_fk_orders_or;
ALTER TABLE IF EXISTS ONLY public.orders_orderitem DROP CONSTRAINT IF EXISTS orders_orderitem_variant_id_5d350ded_fk_shop_variant_id;
ALTER TABLE IF EXISTS ONLY public.orders_orderitem DROP CONSTRAINT IF EXISTS orders_orderitem_order_id_fe61a34d_fk_orders_order_id;
ALTER TABLE IF EXISTS ONLY public.orders_order DROP CONSTRAINT IF EXISTS orders_order_user_id_e9b59eb1_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_group_id_97559544_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
DROP INDEX IF EXISTS public.shop_variant_sku_4800cadf_like;
DROP INDEX IF EXISTS public.shop_variant_product_id_ab80580a;
DROP INDEX IF EXISTS public.shop_product_slug_30bd2d5d_like;
DROP INDEX IF EXISTS public.shop_product_category_id_14d7eea8;
DROP INDEX IF EXISTS public.shop_lot_variant_id_334b69f4;
DROP INDEX IF EXISTS public.shop_lot_code_4f3fa14a_like;
DROP INDEX IF EXISTS public.shop_category_slug_4508178e_like;
DROP INDEX IF EXISTS public.orders_statushistory_order_id_116bfa23;
DROP INDEX IF EXISTS public.orders_statushistory_by_id_5374de9e;
DROP INDEX IF EXISTS public.orders_orderitemallocation_lot_id_0b86825d;
DROP INDEX IF EXISTS public.orders_orderitemallocation_item_id_20193c42;
DROP INDEX IF EXISTS public.orders_orderitem_variant_id_5d350ded;
DROP INDEX IF EXISTS public.orders_orderitem_order_id_fe61a34d;
DROP INDEX IF EXISTS public.orders_order_user_id_e9b59eb1;
DROP INDEX IF EXISTS public.orders_order_code_20afc605_like;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.auth_user_username_6821ab7c_like;
DROP INDEX IF EXISTS public.auth_user_user_permissions_user_id_a95ead1b;
DROP INDEX IF EXISTS public.auth_user_user_permissions_permission_id_1fbb5f2c;
DROP INDEX IF EXISTS public.auth_user_groups_user_id_6a12ed8b;
DROP INDEX IF EXISTS public.auth_user_groups_group_id_97559544;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
ALTER TABLE IF EXISTS ONLY public.shop_variant DROP CONSTRAINT IF EXISTS shop_variant_sku_key;
ALTER TABLE IF EXISTS ONLY public.shop_variant DROP CONSTRAINT IF EXISTS shop_variant_pkey;
ALTER TABLE IF EXISTS ONLY public.shop_product DROP CONSTRAINT IF EXISTS shop_product_slug_key;
ALTER TABLE IF EXISTS ONLY public.shop_product DROP CONSTRAINT IF EXISTS shop_product_pkey;
ALTER TABLE IF EXISTS ONLY public.shop_lot DROP CONSTRAINT IF EXISTS shop_lot_pkey;
ALTER TABLE IF EXISTS ONLY public.shop_lot DROP CONSTRAINT IF EXISTS shop_lot_code_key;
ALTER TABLE IF EXISTS ONLY public.shop_category DROP CONSTRAINT IF EXISTS shop_category_slug_key;
ALTER TABLE IF EXISTS ONLY public.shop_category DROP CONSTRAINT IF EXISTS shop_category_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_statushistory DROP CONSTRAINT IF EXISTS orders_statushistory_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_shipment DROP CONSTRAINT IF EXISTS orders_shipment_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_shipment DROP CONSTRAINT IF EXISTS orders_shipment_order_id_key;
ALTER TABLE IF EXISTS ONLY public.orders_payment DROP CONSTRAINT IF EXISTS orders_payment_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_payment DROP CONSTRAINT IF EXISTS orders_payment_order_id_key;
ALTER TABLE IF EXISTS ONLY public.orders_orderitemallocation DROP CONSTRAINT IF EXISTS orders_orderitemallocation_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_orderitem DROP CONSTRAINT IF EXISTS orders_orderitem_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_order DROP CONSTRAINT IF EXISTS orders_order_pkey;
ALTER TABLE IF EXISTS ONLY public.orders_order DROP CONSTRAINT IF EXISTS orders_order_code_key;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_username_key;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_group_id_94350c0c_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
DROP TABLE IF EXISTS public.shop_variant;
DROP TABLE IF EXISTS public.shop_product;
DROP TABLE IF EXISTS public.shop_lot;
DROP TABLE IF EXISTS public.shop_category;
DROP TABLE IF EXISTS public.orders_statushistory;
DROP TABLE IF EXISTS public.orders_shipment;
DROP TABLE IF EXISTS public.orders_payment;
DROP TABLE IF EXISTS public.orders_orderitemallocation;
DROP TABLE IF EXISTS public.orders_orderitem;
DROP TABLE IF EXISTS public.orders_order;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.auth_user_user_permissions;
DROP TABLE IF EXISTS public.auth_user_groups;
DROP TABLE IF EXISTS public.auth_user;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO odoo;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO odoo;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO odoo;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO odoo;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO odoo;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO odoo;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO odoo;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO odoo;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO odoo;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO odoo;

--
-- Name: orders_order; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.orders_order (
    id bigint NOT NULL,
    code character varying(20) NOT NULL,
    customer_name character varying(120) NOT NULL,
    phone character varying(20) NOT NULL,
    email character varying(254) NOT NULL,
    address text NOT NULL,
    zone character varying(10) NOT NULL,
    note character varying(255) NOT NULL,
    subtotal integer NOT NULL,
    shipping_fee integer NOT NULL,
    total integer NOT NULL,
    status character varying(12) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    user_id integer,
    CONSTRAINT orders_order_shipping_fee_check CHECK ((shipping_fee >= 0)),
    CONSTRAINT orders_order_subtotal_check CHECK ((subtotal >= 0)),
    CONSTRAINT orders_order_total_check CHECK ((total >= 0))
);


ALTER TABLE public.orders_order OWNER TO odoo;

--
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.orders_order ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.orders_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: orders_orderitem; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.orders_orderitem (
    id bigint NOT NULL,
    product_name character varying(200) NOT NULL,
    variant_label character varying(50) NOT NULL,
    unit_price integer NOT NULL,
    quantity integer NOT NULL,
    order_id bigint NOT NULL,
    variant_id bigint NOT NULL,
    CONSTRAINT orders_orderitem_quantity_check CHECK ((quantity >= 0)),
    CONSTRAINT orders_orderitem_unit_price_check CHECK ((unit_price >= 0))
);


ALTER TABLE public.orders_orderitem OWNER TO odoo;

--
-- Name: orders_orderitem_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.orders_orderitem ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.orders_orderitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: orders_orderitemallocation; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.orders_orderitemallocation (
    id bigint NOT NULL,
    quantity integer NOT NULL,
    item_id bigint NOT NULL,
    lot_id bigint NOT NULL,
    CONSTRAINT orders_orderitemallocation_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.orders_orderitemallocation OWNER TO odoo;

--
-- Name: orders_orderitemallocation_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.orders_orderitemallocation ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.orders_orderitemallocation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: orders_payment; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.orders_payment (
    id bigint NOT NULL,
    method character varying(10) NOT NULL,
    status character varying(12) NOT NULL,
    amount integer NOT NULL,
    paid_at timestamp with time zone,
    reference character varying(100) NOT NULL,
    order_id bigint NOT NULL,
    CONSTRAINT orders_payment_amount_check CHECK ((amount >= 0))
);


ALTER TABLE public.orders_payment OWNER TO odoo;

--
-- Name: orders_payment_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.orders_payment ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.orders_payment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: orders_shipment; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.orders_shipment (
    id bigint NOT NULL,
    carrier character varying(80) NOT NULL,
    tracking_code character varying(80) NOT NULL,
    shipped_at timestamp with time zone,
    delivered_at timestamp with time zone,
    order_id bigint NOT NULL
);


ALTER TABLE public.orders_shipment OWNER TO odoo;

--
-- Name: orders_shipment_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.orders_shipment ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.orders_shipment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: orders_statushistory; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.orders_statushistory (
    id bigint NOT NULL,
    from_status character varying(12) NOT NULL,
    to_status character varying(12) NOT NULL,
    note character varying(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    by_id integer,
    order_id bigint NOT NULL
);


ALTER TABLE public.orders_statushistory OWNER TO odoo;

--
-- Name: orders_statushistory_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.orders_statushistory ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.orders_statushistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: shop_category; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.shop_category (
    id bigint NOT NULL,
    name character varying(120) NOT NULL,
    slug character varying(50) NOT NULL,
    "order" smallint NOT NULL,
    CONSTRAINT shop_category_order_check CHECK (("order" >= 0))
);


ALTER TABLE public.shop_category OWNER TO odoo;

--
-- Name: shop_category_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.shop_category ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.shop_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: shop_lot; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.shop_lot (
    id bigint NOT NULL,
    code character varying(40) NOT NULL,
    produced_on date NOT NULL,
    expires_on date NOT NULL,
    quantity_in integer NOT NULL,
    quantity_left integer NOT NULL,
    source_note character varying(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    variant_id bigint NOT NULL,
    CONSTRAINT shop_lot_quantity_in_check CHECK ((quantity_in >= 0)),
    CONSTRAINT shop_lot_quantity_left_check CHECK ((quantity_left >= 0))
);


ALTER TABLE public.shop_lot OWNER TO odoo;

--
-- Name: shop_lot_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.shop_lot ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.shop_lot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: shop_product; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.shop_product (
    id bigint NOT NULL,
    name character varying(200) NOT NULL,
    slug character varying(50) NOT NULL,
    short_description character varying(255) NOT NULL,
    description text NOT NULL,
    ingredients character varying(255) NOT NULL,
    nutrition text NOT NULL,
    origin character varying(200) NOT NULL,
    certificates character varying(255) NOT NULL,
    image character varying(100) NOT NULL,
    is_active boolean NOT NULL,
    is_featured boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    category_id bigint NOT NULL
);


ALTER TABLE public.shop_product OWNER TO odoo;

--
-- Name: shop_product_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.shop_product ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.shop_product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: shop_variant; Type: TABLE; Schema: public; Owner: odoo
--

CREATE TABLE public.shop_variant (
    id bigint NOT NULL,
    label character varying(50) NOT NULL,
    weight_g integer NOT NULL,
    price integer NOT NULL,
    sku character varying(40) NOT NULL,
    is_active boolean NOT NULL,
    product_id bigint NOT NULL,
    CONSTRAINT shop_variant_price_check CHECK ((price >= 0)),
    CONSTRAINT shop_variant_weight_g_check CHECK ((weight_g >= 0))
);


ALTER TABLE public.shop_variant OWNER TO odoo;

--
-- Name: shop_variant_id_seq; Type: SEQUENCE; Schema: public; Owner: odoo
--

ALTER TABLE public.shop_variant ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.shop_variant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.auth_group (id, name) FROM stdin;
1	Sales
2	Warehouse
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
1	1	64
2	1	32
3	1	36
4	1	40
5	1	42
6	1	44
7	1	48
8	1	54
9	1	56
10	1	57
11	1	58
12	1	60
13	2	32
14	2	36
15	2	37
16	2	38
17	2	40
18	2	42
19	2	44
20	2	48
21	2	57
22	2	58
23	2	60
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add Danh mục	7	add_category
26	Can change Danh mục	7	change_category
27	Can delete Danh mục	7	delete_category
28	Can view Danh mục	7	view_category
29	Can add Sản phẩm	8	add_product
30	Can change Sản phẩm	8	change_product
31	Can delete Sản phẩm	8	delete_product
32	Can view Sản phẩm	8	view_product
33	Can add Quy cách	9	add_variant
34	Can change Quy cách	9	change_variant
35	Can delete Quy cách	9	delete_variant
36	Can view Quy cách	9	view_variant
37	Can add Lô hàng	10	add_lot
38	Can change Lô hàng	10	change_lot
39	Can delete Lô hàng	10	delete_lot
40	Can view Lô hàng	10	view_lot
41	Can add Đơn hàng	11	add_order
42	Can change Đơn hàng	11	change_order
43	Can delete Đơn hàng	11	delete_order
44	Can view Đơn hàng	11	view_order
45	Can add Sản phẩm trong đơn	12	add_orderitem
46	Can change Sản phẩm trong đơn	12	change_orderitem
47	Can delete Sản phẩm trong đơn	12	delete_orderitem
48	Can view Sản phẩm trong đơn	12	view_orderitem
49	Can add order item allocation	13	add_orderitemallocation
50	Can change order item allocation	13	change_orderitemallocation
51	Can delete order item allocation	13	delete_orderitemallocation
52	Can view order item allocation	13	view_orderitemallocation
53	Can add Thanh toán	14	add_payment
54	Can change Thanh toán	14	change_payment
55	Can delete Thanh toán	14	delete_payment
56	Can view Thanh toán	14	view_payment
57	Can add Vận chuyển	15	add_shipment
58	Can change Vận chuyển	15	change_shipment
59	Can delete Vận chuyển	15	delete_shipment
60	Can view Vận chuyển	15	view_shipment
61	Can add Lịch sử trạng thái	16	add_statushistory
62	Can change Lịch sử trạng thái	16	change_statushistory
63	Can delete Lịch sử trạng thái	16	delete_statushistory
64	Can view Lịch sử trạng thái	16	view_statushistory
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$1000000$Eq7R1fsh5itBxCsGsSbrTq$Ry07ggWNd+GHtGFkq7+OuBjXGOf8bFzsn4+WFcbNHYg=	\N	t	admin			admin@example.com	t	t	2026-11-09 00:10:29.404984+07
2	pbkdf2_sha256$1000000$Lp8kH1v3AVrQLt7jvt6zso$xU85y3fChU0tQsbJvOexBKFv2qodR+edSZAzLJKCp9I=	\N	f	sales_demo				t	t	2026-11-09 00:10:33.867579+07
3	pbkdf2_sha256$1000000$KvMVpdl39eLk9xQzdu1sIj$FvcKYJWkGpcxTKYccMq2hum1OOs81JflV3VisYWe7CM=	\N	f	warehouse_demo				t	t	2026-11-09 00:10:35.776121+07
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
1	2	1
2	3	2
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	shop	category
8	shop	product
9	shop	variant
10	shop	lot
11	orders	order
12	orders	orderitem
13	orders	orderitemallocation
14	orders	payment
15	orders	shipment
16	orders	statushistory
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-11-09 00:10:12.222227+07
2	auth	0001_initial	2026-11-09 00:10:12.519797+07
3	admin	0001_initial	2026-11-09 00:10:12.597086+07
4	admin	0002_logentry_remove_auto_add	2026-11-09 00:10:12.615111+07
5	admin	0003_logentry_add_action_flag_choices	2026-11-09 00:10:12.63465+07
6	contenttypes	0002_remove_content_type_name	2026-11-09 00:10:12.676041+07
7	auth	0002_alter_permission_name_max_length	2026-11-09 00:10:12.704315+07
8	auth	0003_alter_user_email_max_length	2026-11-09 00:10:12.724921+07
9	auth	0004_alter_user_username_opts	2026-11-09 00:10:12.748379+07
10	auth	0005_alter_user_last_login_null	2026-11-09 00:10:12.772844+07
11	auth	0006_require_contenttypes_0002	2026-11-09 00:10:12.775542+07
12	auth	0007_alter_validators_add_error_messages	2026-11-09 00:10:12.798286+07
13	auth	0008_alter_user_username_max_length	2026-11-09 00:10:12.832431+07
14	auth	0009_alter_user_last_name_max_length	2026-11-09 00:10:12.853959+07
15	auth	0010_alter_group_name_max_length	2026-11-09 00:10:12.876932+07
16	auth	0011_update_proxy_permissions	2026-11-09 00:10:12.907704+07
17	auth	0012_alter_user_first_name_max_length	2026-11-09 00:10:12.927342+07
18	shop	0001_initial	2026-11-09 00:10:13.119534+07
19	orders	0001_initial	2026-11-09 00:10:13.536265+07
20	sessions	0001_initial	2026-11-09 00:10:13.56654+07
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: orders_order; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.orders_order (id, code, customer_name, phone, email, address, zone, note, subtotal, shipping_fee, total, status, created_at, updated_at, user_id) FROM stdin;
\.


--
-- Data for Name: orders_orderitem; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.orders_orderitem (id, product_name, variant_label, unit_price, quantity, order_id, variant_id) FROM stdin;
\.


--
-- Data for Name: orders_orderitemallocation; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.orders_orderitemallocation (id, quantity, item_id, lot_id) FROM stdin;
\.


--
-- Data for Name: orders_payment; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.orders_payment (id, method, status, amount, paid_at, reference, order_id) FROM stdin;
\.


--
-- Data for Name: orders_shipment; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.orders_shipment (id, carrier, tracking_code, shipped_at, delivered_at, order_id) FROM stdin;
\.


--
-- Data for Name: orders_statushistory; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.orders_statushistory (id, from_status, to_status, note, created_at, by_id, order_id) FROM stdin;
\.


--
-- Data for Name: shop_category; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.shop_category (id, name, slug, "order") FROM stdin;
1	Trái cây sấy thăng hoa	trai-cay-say-thang-hoa	1
2	Hạt dinh dưỡng	hat-dinh-duong	2
3	Combo quà tặng	combo-qua-tang	3
\.


--
-- Data for Name: shop_lot; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.shop_lot (id, code, produced_on, expires_on, quantity_in, quantity_left, source_note, created_at, variant_id) FROM stdin;
1	NS01-20G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.862663+07	1
2	NS01-20G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.868295+07	1
3	NS01-20G-L0	2026-10-10	2026-11-24	10	10	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.87234+07	1
4	NS01-20G-LX	2026-10-10	2026-11-04	3	3	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.876366+07	1
5	NS01-50G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.885031+07	2
6	NS01-50G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.889587+07	2
7	NS02-30G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.90925+07	3
8	NS02-30G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.920298+07	3
9	NS02-80G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.935131+07	4
10	NS02-80G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.93854+07	4
11	NS03-50G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.949912+07	5
12	NS03-50G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.95283+07	5
13	NS03-100G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.962583+07	6
14	NS03-100G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.966893+07	6
15	NS04-30G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.979796+07	7
16	NS04-30G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.982949+07	7
17	NS04-80G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.992817+07	8
18	NS04-80G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:28.997234+07	8
19	NS05-50G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.010115+07	9
20	NS05-50G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.013547+07	9
21	NS06-40G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.032401+07	10
22	NS06-40G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.042874+07	10
23	NS07-200G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.066842+07	11
24	NS07-200G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.069736+07	11
25	NS07-500G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.079055+07	12
26	NS07-500G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.084213+07	12
27	NS08-200G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.101648+07	13
28	NS08-200G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.110326+07	13
29	NS08-500G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.12983+07	14
30	NS08-500G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.1409+07	14
31	NS09-250G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.182278+07	15
32	NS09-250G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.192178+07	15
33	NS10-250G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.223163+07	16
34	NS10-250G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.228307+07	16
35	NS11-200G-L1	2026-10-10	2027-03-09	40	40	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.243007+07	17
36	NS11-200G-L2	2026-10-10	2027-09-05	60	60	Dữ liệu mẫu (thay bằng nguồn gốc thật)	2026-11-09 00:10:29.247041+07	17
\.


--
-- Data for Name: shop_product; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.shop_product (id, name, slug, short_description, description, ingredients, nutrition, origin, certificates, image, is_active, is_featured, created_at, category_id) FROM stdin;
1	Dâu tây Đà Lạt sấy thăng hoa	dau-tay-da-lat-say-thang-hoa	Giòn tan, vị chua ngọt của dâu tây Đà Lạt.	Trái cây được làm lạnh sâu rồi hút ẩm trong chân không (sấy thăng hoa) nên giữ được hình dạng, màu sắc và hương vị. Bảo quản nơi khô ráo, đóng kín túi sau khi mở.	Dâu tây	Cập nhật theo kết quả kiểm nghiệm của lô hàng.	Đà Lạt, Lâm Đồng			t	t	2026-11-09 00:10:28.831689+07	1
2	Xoài sấy thăng hoa	xoai-say-thang-hoa	Ngọt thơm, giòn nhẹ, ăn liền hoặc ăn kèm sữa chua.	Trái cây được làm lạnh sâu rồi hút ẩm trong chân không (sấy thăng hoa) nên giữ được hình dạng, màu sắc và hương vị. Bảo quản nơi khô ráo, đóng kín túi sau khi mở.	Xoài	Cập nhật theo kết quả kiểm nghiệm của lô hàng.	Việt Nam			t	t	2026-11-09 00:10:28.898291+07	1
3	Sầu riêng sấy thăng hoa	sau-rieng-say-thang-hoa	Hương sầu riêng đậm, xốp giòn, không dính tay.	Trái cây được làm lạnh sâu rồi hút ẩm trong chân không (sấy thăng hoa) nên giữ được hình dạng, màu sắc và hương vị. Bảo quản nơi khô ráo, đóng kín túi sau khi mở.	Sầu riêng	Cập nhật theo kết quả kiểm nghiệm của lô hàng.	Việt Nam			t	t	2026-11-09 00:10:28.942626+07	1
4	Chuối sấy thăng hoa	chuoi-say-thang-hoa	Chuối sấy giòn, ngọt dịu, hợp làm đồ ăn vặt cho trẻ.	Trái cây được làm lạnh sâu rồi hút ẩm trong chân không (sấy thăng hoa) nên giữ được hình dạng, màu sắc và hương vị. Bảo quản nơi khô ráo, đóng kín túi sau khi mở.	Chuối	Cập nhật theo kết quả kiểm nghiệm của lô hàng.	Việt Nam			t	f	2026-11-09 00:10:28.970683+07	1
5	Mít sấy thăng hoa	mit-say-thang-hoa	Mít sấy giòn xốp, giữ mùi thơm đặc trưng.	Trái cây được làm lạnh sâu rồi hút ẩm trong chân không (sấy thăng hoa) nên giữ được hình dạng, màu sắc và hương vị. Bảo quản nơi khô ráo, đóng kín túi sau khi mở.	Mít	Cập nhật theo kết quả kiểm nghiệm của lô hàng.	Việt Nam			t	f	2026-11-09 00:10:29.001112+07	1
6	Thanh long ruột đỏ sấy thăng hoa	thanh-long-ruot-do-say-thang-hoa	Màu đỏ tự nhiên, vị thanh mát.	Trái cây được làm lạnh sâu rồi hút ẩm trong chân không (sấy thăng hoa) nên giữ được hình dạng, màu sắc và hương vị. Bảo quản nơi khô ráo, đóng kín túi sau khi mở.	Thanh long ruột đỏ	Cập nhật theo kết quả kiểm nghiệm của lô hàng.	Việt Nam			t	f	2026-11-09 00:10:29.017777+07	1
7	Hạt điều rang muối	hat-dieu-rang-muoi	Hạt điều rang giòn, vị béo bùi.	Hạt được chọn lọc, rang chín và đóng gói theo lô. Bảo quản nơi khô ráo, tránh ánh nắng trực tiếp.	Hạt điều, muối	Cập nhật theo kết quả kiểm nghiệm của lô hàng.	Việt Nam			t	t	2026-11-09 00:10:29.058513+07	2
8	Hạt macca nứt vỏ	hat-macca-nut-vo	Macca nứt sẵn vỏ, dễ bóc, béo mịn.	Hạt được chọn lọc, rang chín và đóng gói theo lô. Bảo quản nơi khô ráo, tránh ánh nắng trực tiếp.	Hạt macca	Cập nhật theo kết quả kiểm nghiệm của lô hàng.	Đắk Lắk			t	f	2026-11-09 00:10:29.089885+07	2
9	Mix hạt dinh dưỡng	mix-hat-dinh-duong	Hỗn hợp các loại hạt rang, tiện mang theo.	Hạt được chọn lọc, rang chín và đóng gói theo lô. Bảo quản nơi khô ráo, tránh ánh nắng trực tiếp.	Hạt điều, hạt macca, hạt bí	Cập nhật theo kết quả kiểm nghiệm của lô hàng.	Việt Nam			t	f	2026-11-09 00:10:29.158958+07	2
10	Hộp quà Mùa dâu Đà Lạt	hop-qua-mua-dau-da-lat	Dâu tây sấy thăng hoa và hạt điều trong hộp quà.	Trái cây được làm lạnh sâu rồi hút ẩm trong chân không (sấy thăng hoa) nên giữ được hình dạng, màu sắc và hương vị. Bảo quản nơi khô ráo, đóng kín túi sau khi mở.	Dâu tây, hạt điều	Cập nhật theo kết quả kiểm nghiệm của lô hàng.	Việt Nam			t	t	2026-11-09 00:10:29.204601+07	3
11	Hộp quà Trái cây nhiệt đới	hop-qua-trai-cay-nhiet-doi	Xoài, chuối, mít sấy thăng hoa trong một hộp.	Trái cây được làm lạnh sâu rồi hút ẩm trong chân không (sấy thăng hoa) nên giữ được hình dạng, màu sắc và hương vị. Bảo quản nơi khô ráo, đóng kín túi sau khi mở.	Xoài, chuối, mít	Cập nhật theo kết quả kiểm nghiệm của lô hàng.	Việt Nam			t	f	2026-11-09 00:10:29.23296+07	3
\.


--
-- Data for Name: shop_variant; Type: TABLE DATA; Schema: public; Owner: odoo
--

COPY public.shop_variant (id, label, weight_g, price, sku, is_active, product_id) FROM stdin;
1	20g	20	49000	NS01-20G	t	1
2	50g	50	109000	NS01-50G	t	1
3	30g	30	55000	NS02-30G	t	2
4	80g	80	135000	NS02-80G	t	2
5	50g	50	129000	NS03-50G	t	3
6	100g	100	239000	NS03-100G	t	3
7	30g	30	39000	NS04-30G	t	4
8	80g	80	95000	NS04-80G	t	4
9	50g	50	79000	NS05-50G	t	5
10	40g	40	65000	NS06-40G	t	6
11	200g	200	89000	NS07-200G	t	7
12	500g	500	205000	NS07-500G	t	7
13	200g	200	119000	NS08-200G	t	8
14	500g	500	279000	NS08-500G	t	8
15	250g	250	129000	NS09-250G	t	9
16	Hộp 250g	250	249000	NS10-250G	t	10
17	Hộp 200g	200	229000	NS11-200G	t	11
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 2, true);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 23, true);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 64, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 2, true);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 3, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 16, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 20, true);


--
-- Name: orders_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.orders_order_id_seq', 1, false);


--
-- Name: orders_orderitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.orders_orderitem_id_seq', 1, false);


--
-- Name: orders_orderitemallocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.orders_orderitemallocation_id_seq', 1, false);


--
-- Name: orders_payment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.orders_payment_id_seq', 1, false);


--
-- Name: orders_shipment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.orders_shipment_id_seq', 1, false);


--
-- Name: orders_statushistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.orders_statushistory_id_seq', 1, false);


--
-- Name: shop_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.shop_category_id_seq', 3, true);


--
-- Name: shop_lot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.shop_lot_id_seq', 36, true);


--
-- Name: shop_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.shop_product_id_seq', 11, true);


--
-- Name: shop_variant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: odoo
--

SELECT pg_catalog.setval('public.shop_variant_id_seq', 17, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: orders_order orders_order_code_key; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_code_key UNIQUE (code);


--
-- Name: orders_order orders_order_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_pkey PRIMARY KEY (id);


--
-- Name: orders_orderitem orders_orderitem_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_orderitem
    ADD CONSTRAINT orders_orderitem_pkey PRIMARY KEY (id);


--
-- Name: orders_orderitemallocation orders_orderitemallocation_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_orderitemallocation
    ADD CONSTRAINT orders_orderitemallocation_pkey PRIMARY KEY (id);


--
-- Name: orders_payment orders_payment_order_id_key; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_payment
    ADD CONSTRAINT orders_payment_order_id_key UNIQUE (order_id);


--
-- Name: orders_payment orders_payment_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_payment
    ADD CONSTRAINT orders_payment_pkey PRIMARY KEY (id);


--
-- Name: orders_shipment orders_shipment_order_id_key; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_shipment
    ADD CONSTRAINT orders_shipment_order_id_key UNIQUE (order_id);


--
-- Name: orders_shipment orders_shipment_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_shipment
    ADD CONSTRAINT orders_shipment_pkey PRIMARY KEY (id);


--
-- Name: orders_statushistory orders_statushistory_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_statushistory
    ADD CONSTRAINT orders_statushistory_pkey PRIMARY KEY (id);


--
-- Name: shop_category shop_category_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.shop_category
    ADD CONSTRAINT shop_category_pkey PRIMARY KEY (id);


--
-- Name: shop_category shop_category_slug_key; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.shop_category
    ADD CONSTRAINT shop_category_slug_key UNIQUE (slug);


--
-- Name: shop_lot shop_lot_code_key; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.shop_lot
    ADD CONSTRAINT shop_lot_code_key UNIQUE (code);


--
-- Name: shop_lot shop_lot_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.shop_lot
    ADD CONSTRAINT shop_lot_pkey PRIMARY KEY (id);


--
-- Name: shop_product shop_product_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.shop_product
    ADD CONSTRAINT shop_product_pkey PRIMARY KEY (id);


--
-- Name: shop_product shop_product_slug_key; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.shop_product
    ADD CONSTRAINT shop_product_slug_key UNIQUE (slug);


--
-- Name: shop_variant shop_variant_pkey; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.shop_variant
    ADD CONSTRAINT shop_variant_pkey PRIMARY KEY (id);


--
-- Name: shop_variant shop_variant_sku_key; Type: CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.shop_variant
    ADD CONSTRAINT shop_variant_sku_key UNIQUE (sku);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: orders_order_code_20afc605_like; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX orders_order_code_20afc605_like ON public.orders_order USING btree (code varchar_pattern_ops);


--
-- Name: orders_order_user_id_e9b59eb1; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX orders_order_user_id_e9b59eb1 ON public.orders_order USING btree (user_id);


--
-- Name: orders_orderitem_order_id_fe61a34d; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX orders_orderitem_order_id_fe61a34d ON public.orders_orderitem USING btree (order_id);


--
-- Name: orders_orderitem_variant_id_5d350ded; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX orders_orderitem_variant_id_5d350ded ON public.orders_orderitem USING btree (variant_id);


--
-- Name: orders_orderitemallocation_item_id_20193c42; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX orders_orderitemallocation_item_id_20193c42 ON public.orders_orderitemallocation USING btree (item_id);


--
-- Name: orders_orderitemallocation_lot_id_0b86825d; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX orders_orderitemallocation_lot_id_0b86825d ON public.orders_orderitemallocation USING btree (lot_id);


--
-- Name: orders_statushistory_by_id_5374de9e; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX orders_statushistory_by_id_5374de9e ON public.orders_statushistory USING btree (by_id);


--
-- Name: orders_statushistory_order_id_116bfa23; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX orders_statushistory_order_id_116bfa23 ON public.orders_statushistory USING btree (order_id);


--
-- Name: shop_category_slug_4508178e_like; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX shop_category_slug_4508178e_like ON public.shop_category USING btree (slug varchar_pattern_ops);


--
-- Name: shop_lot_code_4f3fa14a_like; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX shop_lot_code_4f3fa14a_like ON public.shop_lot USING btree (code varchar_pattern_ops);


--
-- Name: shop_lot_variant_id_334b69f4; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX shop_lot_variant_id_334b69f4 ON public.shop_lot USING btree (variant_id);


--
-- Name: shop_product_category_id_14d7eea8; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX shop_product_category_id_14d7eea8 ON public.shop_product USING btree (category_id);


--
-- Name: shop_product_slug_30bd2d5d_like; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX shop_product_slug_30bd2d5d_like ON public.shop_product USING btree (slug varchar_pattern_ops);


--
-- Name: shop_variant_product_id_ab80580a; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX shop_variant_product_id_ab80580a ON public.shop_variant USING btree (product_id);


--
-- Name: shop_variant_sku_4800cadf_like; Type: INDEX; Schema: public; Owner: odoo
--

CREATE INDEX shop_variant_sku_4800cadf_like ON public.shop_variant USING btree (sku varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_order orders_order_user_id_e9b59eb1_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_order
    ADD CONSTRAINT orders_order_user_id_e9b59eb1_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_orderitem orders_orderitem_order_id_fe61a34d_fk_orders_order_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_orderitem
    ADD CONSTRAINT orders_orderitem_order_id_fe61a34d_fk_orders_order_id FOREIGN KEY (order_id) REFERENCES public.orders_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_orderitem orders_orderitem_variant_id_5d350ded_fk_shop_variant_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_orderitem
    ADD CONSTRAINT orders_orderitem_variant_id_5d350ded_fk_shop_variant_id FOREIGN KEY (variant_id) REFERENCES public.shop_variant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_orderitemallocation orders_orderitemallo_item_id_20193c42_fk_orders_or; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_orderitemallocation
    ADD CONSTRAINT orders_orderitemallo_item_id_20193c42_fk_orders_or FOREIGN KEY (item_id) REFERENCES public.orders_orderitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_orderitemallocation orders_orderitemallocation_lot_id_0b86825d_fk_shop_lot_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_orderitemallocation
    ADD CONSTRAINT orders_orderitemallocation_lot_id_0b86825d_fk_shop_lot_id FOREIGN KEY (lot_id) REFERENCES public.shop_lot(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_payment orders_payment_order_id_bdccf250_fk_orders_order_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_payment
    ADD CONSTRAINT orders_payment_order_id_bdccf250_fk_orders_order_id FOREIGN KEY (order_id) REFERENCES public.orders_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_shipment orders_shipment_order_id_661ed8ed_fk_orders_order_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_shipment
    ADD CONSTRAINT orders_shipment_order_id_661ed8ed_fk_orders_order_id FOREIGN KEY (order_id) REFERENCES public.orders_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_statushistory orders_statushistory_by_id_5374de9e_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_statushistory
    ADD CONSTRAINT orders_statushistory_by_id_5374de9e_fk_auth_user_id FOREIGN KEY (by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_statushistory orders_statushistory_order_id_116bfa23_fk_orders_order_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.orders_statushistory
    ADD CONSTRAINT orders_statushistory_order_id_116bfa23_fk_orders_order_id FOREIGN KEY (order_id) REFERENCES public.orders_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shop_lot shop_lot_variant_id_334b69f4_fk_shop_variant_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.shop_lot
    ADD CONSTRAINT shop_lot_variant_id_334b69f4_fk_shop_variant_id FOREIGN KEY (variant_id) REFERENCES public.shop_variant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shop_product shop_product_category_id_14d7eea8_fk_shop_category_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.shop_product
    ADD CONSTRAINT shop_product_category_id_14d7eea8_fk_shop_category_id FOREIGN KEY (category_id) REFERENCES public.shop_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shop_variant shop_variant_product_id_ab80580a_fk_shop_product_id; Type: FK CONSTRAINT; Schema: public; Owner: odoo
--

ALTER TABLE ONLY public.shop_variant
    ADD CONSTRAINT shop_variant_product_id_ab80580a_fk_shop_product_id FOREIGN KEY (product_id) REFERENCES public.shop_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict H4MkmPKBaakhRtarqR8W0TDu5Y0qmc2ven0xfU70s1SfN3BHMnbd9jzpNoEoEs8

