import json
import requests
from typing import Dict, Any
from sqlalchemy import create_engine, text
import redis

class LextitWordPressAutomationBridge:
    """
    Automates data publishing routines into Gutenberg content elements,
    configuring focus fields to preserve layout structure.
    """
    def __init__(self, wp_root_endpoint: str, application_token: str):
        self.endpoint = f"{wp_root_endpoint}/wp-json/wp/v2/posts"
        self.auth_headers = {
            "Authorization": f"Bearer {application_token}",
            "Content-Type": "application/json"
        }

    def deploy_validated_gutenberg_post(self, content_package: Dict[str, Any]) -> bool:
        # Construct clean layout matrices to avoid runtime layout shifts
        compiled_block_markup = (
            f"<h2>Lextit Growth & Conversion Insights</h2>\n"
            f"<p>{content_package['marketing_copy_body']}</p>\n"
            f"<blockquote class='wp-block-quote'><p>{content_package['authority_metric_callout']}</p>"
            f"<cite>Lextit Enterprise Strategy Core</cite></blockquote>\n"
        )

        request_body = {
            "title": content_package.get("headline_title", "Automated Commercial Expansion Matrix"),
            "content": compiled_block_markup,
            "status": "publish",
            "meta": {
                "rank_math_focus_keyword": content_package.get("focus_keyword", ""),
                "rank_math_description": content_package.get("meta_description", "")
            }
        }

        response = requests.post(self.endpoint, json=request_body, headers=self.auth_headers, timeout=12)
        return response.status_code == 201

class LextitWordPressPublisher:
    """
    Handles the asynchronous delivery of AI-generated marketing funnels
    and landing page contents directly to the lextit.com WordPress REST API.
    """
    def __init__(self, site_url: str, application_password: str):
        self.api_url = f"{site_url}/wp-json/wp/v2/posts"
        self.auth_credentials = ('admin_lextit', application_password)

    def publish_marketing_funnel(self, ai_output_json: str) -> bool:
        try:
            payload = json.loads(ai_output_json)

            # Formatting data according to WordPress native core requirements
            wp_payload = {
                "title": payload.get("WP_Post_Title", "Automated Growth Funnel"),
                "content": payload.get("WP_Post_Content", ""),
                "status": "publish", # Can be set to 'draft' for manual review
                "meta": {
                    "seo_title": payload.get("Meta_Title", ""),
                    "seo_description": payload.get("Meta_Description", "")
                }
            }

            response = requests.post(
                self.api_url,
                json=wp_payload,
                auth=self.auth_credentials,
                headers={"Content-Type": "application/json"},
                timeout=15
            )

            return response.status_code == 201
        except Exception as e:
            print(f"[LEXTIT WP-SYNC CRITICAL EXCEPTION] Failed to inject post: {e}")
            return False


class LextitWordPressHydrator:
    """
    Automated engine mapping structured semantic data into semantic,
    production-ready Gutenberg blocks.
    """
    def __init__(self, endpoint_url: str, app_token: str):
        self.api_url = f"{endpoint_url}/wp-json/wp/v2/posts"
        self.headers = {
            "Authorization": f"Bearer {app_token}",
            "Content-Type": "application/json"
        }

    def compile_gutenberg_block_content(self, raw_data: Dict[str, Any]) -> str:
        # Programmatically constructing optimized block infrastructure
        blocks = (
            f"\\n<h1>{raw_data.get('title', '')}</h1>\\n\\n"
            f"\\n<p>{raw_data.get('intro_paragraph', '')}</p>\\n\\n"
            f"\\n"
            f"<blockquote class=\"wp-block-quote\"><p>{raw_data.get('harvard_stat_callout', '')}</p>"
            f"<cite>Lextit Competitive Intelligence Unit</cite></blockquote>\\n\\n"
        )
        return blocks

    def deploy_to_production_site(self, raw_data: Dict[str, Any]) -> bool:
        block_markup = self.compile_gutenberg_block_content(raw_data)
        payload = {
            "title": raw_data.get("title", "Automated Enterprise Asset"),
            "content": block_markup,
            "status": "publish",
            "meta": {
                "seo_focus_keyword": raw_data.get("target_keyword", ""),
                "meta_description": raw_data.get("meta_desc", "")
            }
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=15)
            return response.status_code == 201
        except Exception:
            return False


class LextitDatabaseTuningEngine:
    """
    Automates object caching integration via Redis endpoints and cleans table overhead
    within the WordPress core database to lower asset initialization times.
    """
    def __init__(self, sql_connection_string: str, redis_endpoint: str):
        self.db_engine = create_engine(sql_connection_string, pool_recycle=3600)
        self.cache_client = redis.Redis(host=redis_endpoint, port=6379, db=0)

    def configure_redis_object_cache(self) -> bool:
        """
        Accesses the optimization configurations to set up key-value cache memory blocks,
        reloading the server speed optimization layout.
        """
        try:
            # Emulates W3 Total Cache > Object Cache integration directives
            self.cache_client.set("lextit:config:object_cache", "Redis_Enabled")
            return True
        except Exception as e:
            print(f"[TUNING FAILURE] Redis memory mapping failed: {e}")
            return False

    def purge_redundant_post_revisions(self) -> dict:
        """
        Executes explicit table sweeps to completely drop duplicate post variations
        and clean up database storage structures.
        """
        # Targeted clean queries mapping to Database Cleanup > Optimize Tables workflows
        purge_query = text("DELETE FROM wp_posts WHERE post_type = 'revision';")
        optimize_query = text("OPTIMIZE TABLE wp_posts, wp_postmeta;")

        execution_summary = {"purged_revisions": 0, "status": "FAILED"}

        try:
            with self.db_engine.begin() as transaction:
                # Drop structural duplicate page entries to restore query speed
                result = transaction.execute(purge_query)
                transaction.execute(optimize_query)

                execution_summary["purged_revisions"] = result.rowcount
                execution_summary["status"] = "SUCCESS"
        except Exception as e:
            print(f"[DB PURGE FAILED] {e}")

        return execution_summary
